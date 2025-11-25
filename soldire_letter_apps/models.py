import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db import models, transaction
from django.utils.dateparse import parse_date
from almahdiapp.utils.date import shamsi_to_gregorian
from soldires_apps.utils import map_rank_number_to_choice
from .enums import ClearanceLetterEnum 


class ClearanceLetter(models.Model):
    CLEARANCE_REASON_CHOICES = [
        ('پایان خدمت', 'پایان خدمت'),
        ('قبولی در دانشگاه', 'قبولی در دانشگاه'),
        ('انتقال', 'انتقال'),
        ('معافیت دائم', 'معافیت دائم'),
        ('معافیت کفالت', 'معافیت کفالت'),
    ]
    CLEARANCE_STATUS_CHOICES = [
        ('ایجاد شده', 'ایجاد شده'),
        ('چاپ و درحال بررسی', 'چاپ و درحال بررسی'),
        ('تأیید شده', 'تأیید شده'),
        ('تأیید نهایی', 'تأیید نهایی'),
    ]
    ACTION_CHOICES = [
        ("approve_page_results", "📋 انتخاب گروهی نتایج این صفحه"),
        ("approve_end_service", "🎖️ انتخاب گروهی پایان خدمت"),
        ("approve_transfer", "🔄 انتخاب گروهی انتقالی‌ها"),
        ("approve_uni", "🎓 انتخاب گروهی قبولی در دانشگاه"),
        ("approve_permanent_exemption", "🛂 انتخاب گروهی معافیت دائم"),
        ("approve_temporary_exemption", "⛔ انتخاب گروهی معافیت موقت"),
        ("approve_results", "📋 انتخاب گروهی همه نتایج"),
        ("approve_settlement", "🧾 انتخاب گروهی همه تسویه حساب ها"),
    ]

    soldier = models.ForeignKey('soldires_apps.Soldier', on_delete=models.CASCADE, verbose_name="سرباز")
    reason = models.CharField(max_length=30, choices=CLEARANCE_REASON_CHOICES, verbose_name="علت تسویه حساب")
    letter_number = models.CharField(max_length=100, unique=True, verbose_name="شماره نامه", editable=False)
    issue_date = models.DateField(auto_now_add=True, verbose_name="تاریخ صدور تسویه کل")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    status = models.CharField(max_length=100, choices=CLEARANCE_STATUS_CHOICES, verbose_name="وضعیت نامه", default='ایجاد شده')

    # 🔹 فیلد جدید:
    expired_file_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="شماره پرونده منقضی"
    )
    class Meta:
        verbose_name = "نامه تسویه‌حساب"
        verbose_name_plural = "نامه‌های تسویه‌حساب"

    @property
    def reminde_issue_days(self):
        import logging
        logger = logging.getLogger(__name__)

        """
        تعداد روزهایی که تا تاریخ صدور مانده یا گذشته است.
        - 0 → امروز
        - منفی → برای آینده
        - مثبت → گذشته
        """
        if not self.issue_date:
            return None
        
        today = timezone.now().date()
        delta = today - self.issue_date  # تعداد روز گذشته
        logger.info(f"Delta days: {delta.days}")  # امن و در هر محیط کار می‌کند

        return delta.days
    
    @staticmethod
    def accepted_list(is_accepted=True):
        """
        دریافت نامه‌ها بر اساس وضعیت.
        خروجی QuerySet است و property ها روی هر instance در دسترس هستند.
        """
        status = "تأیید نهایی"
        qs = (ClearanceLetter.objects.filter(status=status) if is_accepted
              else ClearanceLetter.objects.exclude(status=status))
        return qs.order_by('-issue_date')

    @staticmethod
    def get_next_expired_file_number():
        """دریافت شماره پرونده منقضی بعدی به‌صورت اتمیک و یونیک"""
        with transaction.atomic():
            # قفل روی رکوردها برای جلوگیری از رقابت همزمان
            last_number_str = (
                ClearanceLetter.objects
                .select_for_update()
                .order_by('-expired_file_number')
                .values_list('expired_file_number', flat=True)
                .first()
            )

            # اگر رکوردی نبود، از صفر شروع شود
            last_number = int(last_number_str) if last_number_str and last_number_str.isdigit() else 0

            # افزایش شماره
            next_number = last_number + 1

            # برگرداندن به رشته (مثلاً "101")
            return str(next_number)

    def assign_expired_file_number(self, save: bool = True):
        """
        تولید و اختصاص شماره پرونده منقضی.
        اگر save=True باشد، شیء را هم ذخیره می‌کند.
        """
        self.expired_file_number = ClearanceLetter.get_next_expired_file_number()
        if save:
            self.save(update_fields=['expired_file_number'])
        return self.expired_file_number

    @staticmethod
    def get_between_dates(start_date=None, end_date=None):
        """
        دریافت نامه‌ها بین دو تاریخ. ساعت نادیده گرفته می‌شود.
        تاریخ‌های نامعتبر یا خالی به‌صورت خودکار با اولین یا آخرین تاریخ موجود جایگزین می‌شوند.
        """

        # دریافت حداقل و حداکثر تاریخ موجود
        dates = ClearanceLetter.objects.aggregate(
            first_date=models.Min("issue_date"),
            last_date=models.Max("issue_date")
        )

        first_date = dates["first_date"]
        last_date = dates["last_date"]

        # اگر هیچ نامه‌ای وجود نداشت
        if not first_date or not last_date:
            return ClearanceLetter.objects.none()

        # تبدیل string به date اگر لازم باشد
        if isinstance(start_date, str):
            start_date = parse_date(start_date)
        if isinstance(end_date, str):
            end_date = parse_date(end_date)

        # جایگزینی تاریخ‌های نامعتبر یا خالی
        if not start_date:
            start_date = first_date
        if not end_date:
            end_date = last_date

        # اصلاح بازه اگر برعکس باشد
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        if start_date == end_date:
            return ClearanceLetter.objects.filter(issue_date=start_date).order_by('-issue_date')

        return ClearanceLetter.objects.filter(issue_date__gte=start_date,issue_date__lte=end_date).order_by('-issue_date')

    def __str__(self):
        return f"{self.soldier} - {self.get_reason_display()} - {self.letter_number}"

    def save(self, *args, **kwargs):
        if self.letter_number and ClearanceLetter.objects.filter(letter_number=self.letter_number).exclude(pk=self.pk).exists():
            self.letter_number = None
        
        if not self.letter_number:
            # فرض بر این است که Soldier دارای فیلد national_code می‌باشد
            national_code = self.soldier.national_code[-4:]  # ۴ رقم آخر کد ملی
            date_part = timezone.now().strftime('%Y%m%d')  # تاریخ به صورت YYYYMMDD
            self.letter_number = f"CL-{national_code}-{date_part}"
            # اطمینان از یونیک بودن:
            counter = 1
            base_letter_number = self.letter_number
            while ClearanceLetter.objects.filter(letter_number=self.letter_number).exists():
                self.letter_number = f"{base_letter_number}-{counter}"
                counter += 1
            
        if not self.expired_file_number:
            self.assign_expired_file_number(save=False)

        super().save(*args, **kwargs)
        if self.soldier:
            if self.expired_file_number:
                self.soldier.expired_file_number = self.expired_file_number  
            self.soldier.is_checked_out = True
            self.soldier.save()

    @staticmethod
    def save_record(record: dict):
        """
        ایجاد یا بروزرسانی یک رکورد ClearanceLetter از دیکشنری
        بازگشت:
            {'obj': instance_or_None, 'created': bool, 'updated': bool, 'error': str_or_None}
        """
        try:

            # ============ 1) دریافت کد ملی از اکسل ============
            soldier_code = record.get('nationalCode')
            if not soldier_code:
                return {
                    'obj': None, 'created': False, 'updated': False,
                    'error': 'کد ملی سرباز وجود ندارد.'
                }

            # ============ 2) پیدا کردن یا ساختن سرباز ============
            try:
                # پس تاریخ است → باید تبدیل شود
                finished_at = shamsi_to_gregorian(record.get('finishedAt'))
            except:
                finished_at = None
            soldier, created, err = Soldier.create_minimal_from_import(
                national_code=soldier_code,
                first_name=record.get('firstName', ''),
                last_name=record.get('lastName', ''),
                degree_number=record.get('degree'),
                expired_file_number=record.get('expiredFileNumber'),
                finished_at =finished_at
            )
            if soldier:
                soldier.to_checkout()

            print(err)

            if err:
                return {
                    'obj': None, 'created': False, 'updated': False,
                    'error': err
                }

            # ============ 3) شماره نامه ============
            letter_number = record.get('letterNumber')
            # ============ 4) تاریخ‌ها (تبدیل به میلادی) ============
            try:
                issued_at = shamsi_to_gregorian(record.get('issuedAt'))
            except:
                issued_at = None
                
            # ============ 5) تعیین reason بر اساس finishedAt اگر تاریخ نبود ============
            reason = record.get('reason', 'پایان خدمت') 
            finished_at_raw = record.get('finishedAt')
            # finishedAt ممکن است یکی از موارد زیر باشد:
            # 1) تاریخ شمسی → باید تبدیل شود
            # 2) یکی از مقادیر CHOICES → باید به عنوان reason استفاده شود
            CHOICE_KEYS = [c[0] for c in ClearanceLetter.CLEARANCE_REASON_CHOICES]

            if finished_at_raw in CHOICE_KEYS:
                # یعنی این مقدار دلیل است نه تاریخ
                reason = finished_at_raw
                finished_at = None
            
            # ============ 6) ساخت defaults برای ذخیره ============
            defaults = {
                'letter_number':letter_number,
                'soldier': soldier,
                'issue_date': issued_at,
                'description': record.get('description', ''),
                'reason': reason,
                'status': record.get('reason', 'تأیید نهایی'),
                'expired_file_number': record.get('expiredFileNumber') or '00 خالی 00',
            }
            # ============ 7) ذخیره یا بروزرسانی ============
            obj, created = ClearanceLetter.objects.update_or_create(
                soldier__national_code=soldier_code,
                defaults=defaults
            )
            print(obj,"===== ",created)
            return {
                'obj': obj,
                'created': created,
                'updated': not created,
                'error': None
            }

        except Exception as e:
            print('Error',str(e))
            return {
                'obj': None, 'created': False, 'updated': False,
                'error': str(e)
            }
    @classmethod
    def import_data(cls, records):
        """
        پردازش لیستی از رکوردهای ClearanceLetter.
        records: لیست دیکشنری‌ها
        خروجی: {'created': n, 'updated': m, 'errors': [...]}
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


class NormalLetter(models.Model):
    STATUS_CHOICES = [
        ('ایجاد شده', 'ایجاد شده'),
        ('چاپ و بررسی شده', 'چاپ و بررسی شده'),
        ('تایید شده', 'تایید شده'),
    ]

    LETTER_TYPE_CHOICES = [
        ('membership', 'گواهی عضویت'),
        ('service', 'گواهی اشتغال به خدمت'),
        ('request', 'نامه درخواست'),
        ('سنجش و ارزیابی سلامت روان', 'سنجش و ارزیابی سلامت روان'),
        ('other', 'سایر'),
    ]

    soldier = models.ForeignKey('soldires_apps.Soldier', on_delete=models.CASCADE, verbose_name='سرباز')
    letter_number = models.CharField(max_length=30, unique=True, editable=False, verbose_name='شماره نامه')
    letter_type = models.CharField(max_length=250, choices=LETTER_TYPE_CHOICES, verbose_name='نوع نامه')
    date = models.DateField(auto_now_add=True, verbose_name='تاریخ نامه')
    destination = models.CharField(max_length=255, verbose_name='مقصد نامه')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='ایجاد شده', verbose_name='وضعیت نامه')
    created_by = models.ForeignKey('accounts_apps.MyUser', on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name='ایجادکننده')

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.letter_number:
            self.letter_number = self.generate_letter_number()
        super().save(*args, **kwargs)

    def generate_letter_number(self):
        # ترکیب تاریخ و ID موقتی برای شماره یکتا
        date_str = timezone.now().strftime('%y%m%d')
        last_id = (NormalLetter.objects.aggregate(models.Max('id'))['id__max'] or 0) + 1
        return f"LTR-{date_str}-{last_id:05d}"

    def __str__(self):
        return f'{self.letter_number} - {self.get_letter_type_display()} - {self.soldier}'

    class Meta:
        verbose_name = "نامه"
        verbose_name_plural = "نامه‌ها"


class NormalLetterMentalHealthAssessmentAndEvaluation(models.Model):
    SUBJECT_CHOICES = [
        ('entry_test', 'تست سلامت بدو ورود'),
        ('return_test', 'تست سلامت پس از بازگشت از فرار'),
    ]

    normal_letter = models.OneToOneField(
        'soldire_letter_apps.NormalLetter',
        on_delete=models.CASCADE,
        verbose_name='نامه عادی'
    )
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, verbose_name='موضوع')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def is_due_for_retest(self):
        """بررسی اینکه آیا 6 ماه از این تست گذشته یا نه"""
        return timezone.now() >= self.created_at + timedelta(days=180)

    class Meta:
        verbose_name = 'تست سلامت روان'
        verbose_name_plural = 'تست‌های سلامت روان'


class NormalLetterJudicialInquiry(models.Model):
    REASON_CHOICES = [
        ('پایان خدمت', 'پایان خدمت'),
        ('قبولی در دانشگاه', 'قبولی در دانشگاه'),
        ('ماه پایانی خدمت', 'ماه پایانی خدمت'),
        ('معافیت پزشکی', 'معافیت پزشکی'),
        ('انتقال', 'انتقال'),
    ]

    normal_letter = models.OneToOneField('soldire_letter_apps.NormalLetter', on_delete=models.CASCADE,
                                         verbose_name='نامه عادی')
    reason = models.CharField(max_length=30, choices=REASON_CHOICES, verbose_name='علت استعلام')
    subject = models.CharField(max_length=255, verbose_name='موضوع')

    class Meta:
        verbose_name = 'استعلام قضایی'
        verbose_name_plural = 'استعلام‌های قضایی'

    def __str__(self):
        return f"{self.get_reason_display()} - {self.subject}"


class NormalLetterDomesticSettlement(models.Model):
    REASON_CHOICES = [
        ('پایان خدمت', 'پایان خدمت'),
        ('قبولی در  دانشگاه', 'قبولی در  دانشگاه'),
        ('جابجایی', 'جابجایی'),
        ('انتقال', 'انتقال'),
        ('معافیت کفالت', 'معافیت کفالت'),

    ]
    reason = models.CharField(max_length=30, choices=REASON_CHOICES, verbose_name='علت تسویه حساب')
    subject = models.CharField(max_length=255, verbose_name='موضوع')
    normal_letter = models.OneToOneField('soldire_letter_apps.NormalLetter', on_delete=models.CASCADE,
                                         verbose_name='نامه عادی')

    class Meta:
        verbose_name = 'تسویه حساب داخلی'
        verbose_name_plural = 'تسویه حساب های داخلی'

    def __str__(self):
        return f'{self.get_reason_display()} - {self.subject}'

from enum import Enum
class IntroductionLetterType(Enum):
    I =     'معرفی‌نامه'
    L5 =    'پنج‌برگ'
    L5I =   'پنج‌برگ+معرفی‌نامه'

class IntroductionLetter(models.Model):
    LETTER_TYPE_CHOICES = [
        (IntroductionLetterType.I.value, 'معرفی‌نامه'),
        (IntroductionLetterType.L5.value, 'پنج برگ'),
        (IntroductionLetterType.L5I.value, 'پنج برگ + معرفی نامه'),
    ]

    STATUS_CHOICES = [
        ('ایجاد شده', 'ایجاد شده'),
        ('چاپ و درحال بررسی', 'چاپ و درحال بررسی'),
        ('تأیید نهایی', 'تأیید نهایی'),
    ]

    letter_number = models.CharField(max_length=50, unique=True, verbose_name="شماره نامه")
    letter_date = models.DateField(auto_now_add=True, verbose_name="تاریخ نامه")
    soldier = models.ForeignKey("soldires_apps.Soldier", on_delete=models.CASCADE, verbose_name="سرباز")
    part = models.ForeignKey('units_apps.ParentUnit', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name="قسمت معرفی‌شده")
    sub_part = models.ForeignKey('units_apps.SubUnit', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="زیرقسمت")
    letter_type = models.CharField(max_length=20, choices=LETTER_TYPE_CHOICES, default='معرفی‌نامه',
                                   verbose_name="نوع نامه")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ایجاد شده', verbose_name="وضعیت")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین تغییر")

    def __str__(self):
        return f"{self.letter_number} - {self.soldier}"

    class Meta:
        verbose_name = "معرفی نامه"
        verbose_name_plural = "معرفی نامه ها"

    def save(self, *args, **kwargs):
        if not self.letter_number:
            self.letter_number = self.generate_letter_number()
        super().save(*args, **kwargs)

    def generate_letter_number(self):
        # می‌تونی اینجا فرمت دلخواهت رو تعریف کنی مثلاً با تاریخ یا شماره تصادفی
        return f"LT-{uuid.uuid4().hex[:8]}"


class MembershipCertificate(models.Model):
    SUBJECT_CHOICES = [
        ('گواهی عضویت', 'گواهی عضویت'),
        ('گواهی پایان خدمت', 'گواهی پایان خدمت'),
        ('گواهی پایان دوره آموزش', 'گواهی پایان دوره آموزش'),
        ('تسویه حساب', 'تسویه حساب'),
    ]

    normal_letter = models.OneToOneField(
        'soldire_letter_apps.NormalLetter',
        on_delete=models.CASCADE,
        verbose_name='نامه عادی'
    )

    soldier = models.ForeignKey(
        'soldires_apps.Soldier',
        on_delete=models.CASCADE,
        verbose_name="سرباز"
    )

    subject = models.CharField(
        max_length=250,
        choices=SUBJECT_CHOICES,
        verbose_name="موضوع"
    )

    description_in = models.TextField(
        blank=True,
        null=True,
        verbose_name="توضیحات داخل نامه"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="توضیحات"
    )

    def __str__(self):
        return f"{self.soldier} - {self.subject}"

    class Meta:
        verbose_name = "نامه گواهی"
        verbose_name_plural = "نامه‌های گواهی"
        ordering = ['-id']


class NormalLetterHealthIodine(models.Model):
    part = models.ForeignKey('units_apps.ParentUnit', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name="قسمت معرفی‌شده")
    sub_part = models.ForeignKey('units_apps.SubUnit', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="زیرقسمت")
    normal_letter = models.OneToOneField(
        'soldire_letter_apps.NormalLetter',
        on_delete=models.CASCADE,
        verbose_name='نامه عادی'
    )

    class Meta:
        verbose_name = "نامه  تائیدیه سلامت"
        verbose_name_plural = "نامه‌های  تائیدیه سلامت"


class NormalLetterCommitmentLetter(models.Model):
    normal_letter = models.OneToOneField(
        'soldire_letter_apps.NormalLetter',
        on_delete=models.CASCADE,
        verbose_name='نامه عادی'
    )
    CARD_CHIP_CHOICES = [('کارت', 'کارت'), ('تراشه', 'تراشه')]
    type_card_chip = models.CharField(max_length=100, choices=CARD_CHIP_CHOICES, null=True, blank=True,
                                      verbose_name='تراشه/کارت')

    class Meta:
        verbose_name = "تعهد نامه"
        verbose_name_plural = "تعهد نامه"

    def __str__(self):
        return f"{self.normal_letter} - {self.type_card_chip}"

from django.db import models
from django.utils import timezone
from soldires_apps.models import Soldier
from django.db import transaction

class RunawayLetter(models.Model):
    STATUS_CHOICES = [
        ('ایجاد شده', 'ایجاد شده'),
        ('چاپ و درحال بررسی', 'چاپ و درحال بررسی'),
        ('تأیید نهایی', 'تأیید نهایی'),
    ]

    normal_letter = models.OneToOneField(
        NormalLetter,
        on_delete=models.CASCADE,
        verbose_name='نامه عادی',
        blank=True,
        null=True
    )

    soldier = models.ForeignKey(
        Soldier,
        on_delete=models.CASCADE,
        verbose_name="سرباز"
    )

    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='ایجاد شده', verbose_name="وضعیت نامه")
    letter_date = models.DateField(auto_now_add=True, verbose_name="تاریخ ثبت فرار")
    absence_start_date = models.DateField(verbose_name="تاریخ شروع غیبت")
    absence_end_date = models.DateField(blank=True, null=True, verbose_name="تاریخ پایان غیبت")
    letter_number = models.CharField(max_length=50, unique=True, verbose_name="شماره نامه", editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین تغییر')
    class Meta:
        verbose_name = "نامه فرار"
        verbose_name_plural = "نامه‌های فرار"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.letter_number} - {self.soldier}"


    def save(self, *args, **kwargs):
        with transaction.atomic():
            # اگر شماره نامه یکتا نساخته شده باشد، بساز
            if not self.letter_number:
                today = timezone.now().strftime("%y%m%d")
                last_item = RunawayLetter.objects.order_by('-id').first()
                next_id = (last_item.id + 1) if last_item else 1
                self.letter_number = f"ESC-{today}-{next_id:05d}"
            # ساخت یا بروزرسانی NormalLetter مرتبط
            if not self.normal_letter:
                normal_letter = NormalLetter.objects.create(
                    soldier=self.soldier,
                    letter_type='گزارش غیبت منجر به فرار',
                    destination='آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه - مدیریت نیروی انسانی - قضایی و انضباطی ',
                    description=self.description,
                )
                self.normal_letter = normal_letter
            else:
                self.normal_letter.description = self.description
                self.normal_letter.save()

            super().save(*args, **kwargs)

            # اگر وضعیت تأیید نهایی شد، سرباز به حالت فراری تغییر می‌کند
            if self.status == 'تأیید نهایی':
                self.soldier.is_fugitive = True
                self.soldier.save()

from django.db import models
from django.utils import timezone
from django.core.paginator import Paginator
import json
class EssentialFormQuerySet(models.QuerySet):
    def loads_data(self):
        for obj in self:
            if isinstance(obj.form_data, str):
                try:
                    obj.form_data = json.loads(obj.form_data)
                except json.JSONDecodeError:
                    obj.form_data = {}
        return self

    def paginate(self, page=1, per_page=50):
        paginator = Paginator(self, per_page)
        return paginator.get_page(page)


class EssentialFormManager(models.Manager):
    def get_queryset(self):
        return EssentialFormQuerySet(self.model, using=self._db)

    def paginate(self, query, page=1, per_page=50):
        qs = query.loads_data()
        return qs.paginate(page, per_page)

class EssentialFormCardLetter(models.Model):
    objects = EssentialFormManager()
    # انتخاب نوع فرم / نامه
    LETTER_TYPES = [
        ('clearance_letter', 'فرم شماره 3'),
        ('officer_card', 'صدور کارت پایور'),
        ('soldier_card', 'صدور کارت سرباز'),
        ('checkout_3plus', 'فرم تسویه حساب 3 فرزندی و بالاتر'),
        ('activate_old_staff', 'فعال سازی اعزام کارکنان قدیمی'),
        ('certificate_two_guard', 'گواهی دو پاسدار'),
        ('permanent_exemption', 'معافیت دائم کارکنان وظیفه'),
    ]

    # فیلدهای عمومی همه فرم‌ها
    number = models.CharField(max_length=50, help_text="شماره نامه", blank=True, null=True)
    return_number = models.CharField(max_length=50, help_text="شماره ارجاع/بازگشت", blank=True, null=True)
    sender = models.CharField(max_length=200, help_text="از", blank=True, null=True)
    receiver = models.CharField(max_length=200, help_text="به", blank=True, null=True)
    title = models.CharField(max_length=200, help_text="عنوان نامه", blank=True)
    letter_type = models.CharField(
        max_length=50,
        choices=LETTER_TYPES,
        null=False,
        blank=False,
        help_text="نوع فرم/نامه"
    )
    description = models.TextField(blank=True, null=True, help_text="توضیحات اضافی نامه")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # اطلاعات اختصاصی هر فرم به صورت JSON
    form_data = models.JSONField(blank=True, null=True, help_text="ذخیره داده‌های فرم به صورت JSON")

    class Meta:
        verbose_name = "فرم ضروری صدور کارت"
        verbose_name_plural = "فرم‌های ضروری صدور کارت"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_letter_type_display()} - {self.title or 'بدون عنوان'}"

    def loads_form_data(self):
        """
        تبدیل form_data به dict اگر string ذخیره شده باشد.
        خروجی: dict برمی‌گرداند.
        """
        if isinstance(self.form_data, str):
            try:
                self.form_data = json.loads(self.form_data)
            except json.JSONDecodeError:
                self.form_data = {}
        return self.form_data

    @classmethod
    def paginate(cls, query, page=1, counts=50):
        """
        دریافت queryset و برگرداندن صفحه‌ی مشخص
        خروجی: page_obj
        """
        paginator = Paginator(query, counts)
        return paginator.get_page(page)
    

from django.db import models

class ReadyForms(models.Model):
    label = models.CharField(max_length=255, verbose_name="عنوان فرم")
    file = models.FileField(upload_to='ready_forms/files/', verbose_name="فایل فرم")
    image = models.ImageField(upload_to='ready_forms/images/', blank=True, null=True, verbose_name="تصویر فرم")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    helper_text = models.TextField(blank=True, null=True, verbose_name="متن راهنما")
    
    FILE_TYPES = [
        ('pdf', 'پی دی اف'),
        ('docx', 'ورد'),
        ('xlsx', 'اکسل'),
        ('txt', 'متنی'),
        ('image', 'تصویر'),
    ]

    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='pdf', verbose_name="نوع فایل")
    PAGE_SIZES = [
        ('A4', 'A4'),
        ('Letter', 'Letter'),
        ('Legal', 'Legal'),
        ('A3', 'A3'),
        ('A5', 'A5'),
    ]
    page_size = models.CharField(max_length=10, choices=PAGE_SIZES, default='A4', verbose_name="نوع صفحه")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "فرم آماده"
        verbose_name_plural = "فرم‌های آماده"

    def __str__(self):
        return self.label
