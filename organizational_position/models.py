from django.db import models
from django.utils import timezone
from soldires_apps.models import Soldier
from django.utils import timezone
from django.db import transaction

class OrganizationalPosition(models.Model):
    """
        مدل جایگاه سازمانی
        فیلد position_code بازدارندهٔ تکرار، non-null و non-blank است.
    """
    position_code = models.CharField(max_length=50,unique=True,null=False,blank=False,verbose_name="کد جایگاه")
    position_group = models.CharField(max_length=100,blank=True,null=True,verbose_name="گروه جایگاه")
    position_parent_group = models.CharField(max_length=100,blank=True,null=True,verbose_name="سرگروه جایگاه")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="عنوان جایگاه")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    # 
    soldier = models.OneToOneField(
        'soldires_apps.Soldier',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='سرباز دارنده جایگاه فعلی',
        related_name='last_solider'
    )
    
    class Meta:
        verbose_name = "جایگاه سازمانی"
        verbose_name_plural = "جایگاه‌های سازمانی"
        ordering = ['position_code']

    def __str__(self):
        return f"{self.position_code} - {self.title or ''}"
    # ======================
    # توابع شمارشی و بازیابی سربازان
    # فرض: Soldier.position.related_name == 'soldiers'
    # ======================
    @property
    def soldiers(self):
        return Soldier.objects
    @property
    def soldiers_all(self):
        return self.soldiers.filter(position__isnull=False)
    @property
    def soldiers_previous(self):
        return self.soldiers_all(is_checked_out=True)
    @property
    def soldiers_now(self):
        return self.soldiers_all(is_checked_out=False)
    @property
    def soldiers_previous_counts(self):
        return self.soldiers_previous.count()
    @property
    def soldiers_now_counts(self):
        return self.soldiers_now.count()
    @property
    def soldiers_all_counts(self):
        return self.soldiers_all.count()
    # ======================
    # عملیات واردسازی و تخصیص
    # ======================
    @classmethod
    def save_record(cls, record):
        """
        ذخیره یا بروزرسانی یک رکورد جایگاه سازمانی.
        record می‌تواند dict یا tuple/list باشد:
          - dict: {"position_code": "...", "position_group": "...", "title": "..."}
          - tuple/list: ("P001", "GroupA", "عنوان")
        بازگشت: dict با وضعیت ذخیره:
            {'created': True/False, 'updated': True/False, 'error': None یا متن خطا, 'obj': instance}
        """
        try:
            print(record)
            if isinstance(record, (list, tuple)):
                position_code = str(record[0])
                position_group = record[1] if len(record) > 1 else None
                position_parent_group = record[2] if len(record) > 2 else None
                title = record[3] if len(record) > 3 else None
                defaults = {
                    'position_group': position_group, 
                    'title': title,
                    'position_parent_group':position_parent_group
                }
            elif isinstance(record, dict):
                position_code = str(record.get('position_code') or record.get('code') or record['position_code'])
                defaults = {
                    'position_group': record.get('position_group'),
                    'position_parent_group':record.get('position_parent_group'),
                    'title': record.get('title')
                }
            else:
                raise ValueError("record must be dict or tuple/list")

            obj, created_flag = cls.objects.update_or_create(
                position_code=position_code,
                defaults={k: v for k, v in defaults.items() if v is not None}
            )

            return {
                'created': created_flag,
                'updated': not created_flag,
                'error': None,
                'obj': obj
            }

        except Exception as e:
            return {
                'created': False,
                'updated': False,
                'error': str(e),
                'obj': None
            }

    @classmethod
    def import_data(cls, records):
        """
        وارد کردن/به‌روزرسانی جایگاه‌ها با استفاده از save_record.
        records می‌تواند لیستی از دیکشنری‌ها یا تاپل‌ها باشد:
        - دیکشنری: {"position_code": "P001", "position_group": "GroupA", "title": "..."}
        - تاپل: ("P001", "GroupA", "عنوان")  — در این حالت position_group اختیاری است.
        بازگشت: {'created': n, 'updated': m, 'errors': [...]}
        """
        created = 0
        updated = 0
        errors = []

        for rec in records:
            result = cls.save_record(rec)
            if result['error']:
                errors.append({'record': rec, 'error': result['error']})
            else:
                if result['created']:
                    created += 1
                elif result['updated']:
                    updated += 1

        return {'created': created, 'updated': updated, 'errors': errors}
    

    @classmethod
    def assign_soldier(cls, soldier, position):
        """
        تخصیص یک سرباز به یک جایگاه مشخص.
        ورودی‌ها:
            soldier: نمونه‌ای از مدل Soldier
            position: نمونه‌ای از مدل OrganizationalPosition
        خروجی:
            دیکشنری شامل وضعیت و پیام نتیجه
        """
        try:
            if not soldier:
                raise ValueError("سرباز معتبر ارسال نشده است.")
            if not position:
                raise ValueError("جایگاه معتبر ارسال نشده است.")

            # انجام تخصیص
            soldier.position = position
            soldier.position_at = timezone.now().date()
            soldier.save()
            position.soldier = soldier
            position.save()
            
            return {
                'status': 'assigned',
                'soldier': soldier.national_code if hasattr(soldier, 'national_code') else soldier.pk,
                'position': position.position_code if hasattr(position, 'position_code') else position.pk
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'soldier': getattr(soldier, 'national_code', None),
                'position': getattr(position, 'position_code', None)
            }

    @classmethod
    def assign_soldiers(cls, records):
        """
        تخصیص گروهی سربازان به جایگاه‌ها بر اساس لیست رکوردها.
        هر رکورد باید شامل (position_code, national_code) باشد.
        """
        assigned = 0
        not_found_soldiers = []
        not_found_positions = []
        errors = []

        with transaction.atomic():
            for rec in records:
                try:
                    print(rec)
                    # پشتیبانی از انواع ورودی (dict / list / tuple)
                    if isinstance(rec, (list, tuple)):
                        pos_code, national_code = rec
                    elif isinstance(rec, dict):
                        pos_code = rec.get('position_code') or rec.get('pos')
                        national_code = rec.get('national_code') or rec.get('nid') or rec.get('code')
                    else:
                        raise ValueError("record must be dict or tuple/list")

                    # بررسی مقادیر خالی
                    if not pos_code or not national_code:
                        errors.append({'record': rec, 'error': 'missing position_code or national_code'})
                        continue

                    # یافتن سرباز
                    soldier = Soldier.objects.filter(national_code=str(national_code).strip()).first()
                    if not soldier:
                        not_found_soldiers.append(national_code)
                        continue

                    # یافتن جایگاه
                    position = cls.objects.filter(position_code=str(pos_code).strip()).first()
                    if not position:
                        not_found_positions.append(pos_code)
                        continue

                    # تخصیص از طریق متد اصلی
                    result = cls.assign_soldier(soldier, position)
                    status = result.get('status')
                    if result.get('') == 'assigned':
                        assigned += 1
                    elif status == 'error':
                        errors.append({'record': rec, 'error': result.get('error')})

                except Exception as e:
                    errors.append({'record': rec, 'error': str(e)})

        return {
            'assigned': assigned,
            'not_found_soldiers': list(set(not_found_soldiers)),
            'not_found_positions': list(set(not_found_positions)),
            'errors': errors,
        }