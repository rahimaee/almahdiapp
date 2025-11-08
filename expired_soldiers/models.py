from django.db import models
from django.db.models import Q
import jdatetime
from datetime import datetime
from django.core.exceptions import ValidationError
import math
from django.db import transaction
import re
from .enums import * 

class ExpiredSoldier(models.Model):
    description = models.CharField(max_length=500, blank=True,verbose_name="توضیحات",default='')
    expired_file_number = models.CharField(max_length=50, null=True, blank=True,verbose_name="شماره پرونده منقضی",default='')
    expired_file = models.CharField(max_length=50, null=True, blank=True,verbose_name="پرونده",default='')
    organization_code = models.CharField(null=True,blank=True,max_length=15,verbose_name="کد سربازی"  )
    first_name = models.CharField(max_length=50,verbose_name="نام",default='')
    last_name = models.CharField(max_length=50,verbose_name="نام و نام خانوادگی",default='')
    father_name = models.CharField(max_length=50,verbose_name="نام پدر",default='')
    
    @property 
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property 
    def person_of_father(self):
        return f"{self.first_name} {self.last_name} فرزند {self.father_name}"
    
    national_code = models.CharField(max_length=15,null=True,blank='true',default='',verbose_name="کد ملی")
    birth_certificate_number = models.CharField(null=True,blank=True,max_length=15,verbose_name="شماره شناسنامه",default='')  
    start_service_date = models.DateField(null=True,blank=True,verbose_name="تاریخ شروع خدمت سربازی")
    runaway_date = models.DateField(null=True,blank=True,verbose_name="تاریخ فرار از سربازی")
    end_service_date = models.DateField(null=True,blank=True,verbose_name="تاریخ پایان خدمت سربازی")
    settlement_date = models.DateField(null=True,blank=True,verbose_name="تاریخ تسویه سرباز")
    expired_reason = models.CharField(max_length=50, choices=EXPIRED_REASON_CHOICES, null=True, blank=True, verbose_name="دلیل منقضی شدن",default='')
    
    
    @property
    def expired_reason_label(self):
        """
        برگرداندن متن فارسی دلیل منقضی شدن
        """
        if not self.expired_reason:
            return "منقضی از خدمت"
        return ExpiredReasonEnum(self.expired_reason).label

    @property
    def expired_reason_color(self):
        """
        برگرداندن رنگ مناسب badge برای هر دلیل
        """
        color_map = {
            ExpiredReasonEnum.END_OF_SERVICE: "success",
            ExpiredReasonEnum.ESCAPE: "danger",
            ExpiredReasonEnum.STUDY: "info",
            ExpiredReasonEnum.DEATH: "danger",
            ExpiredReasonEnum.TRANSFER_DUTY: "primary",
            ExpiredReasonEnum.TRANSFER: "warning",
            ExpiredReasonEnum.DUTY: "dark",
            ExpiredReasonEnum.EXPIRED: "secondary",
        }
        return color_map.get(self.expired_reason, "secondary")
    
    review_status = models.CharField( null=True,blank=True,max_length=20,verbose_name="بررسی وضعیت",default='')
    status = models.CharField( null=True,blank=True,max_length=20,verbose_name="وضعیت",default='')


    def __str__(self):
        return f"{self.full_name} - {self.national_code}"

    class Meta:
        verbose_name = "سرباز منقضی خدمت"
        verbose_name_plural = "سربازان منقضی خدمت"
        ordering  = ['-expired_file_number']
        

    @classmethod
    def search(cls, query=None, count=10):
        try:
            count = int(count)
        except (ValueError, TypeError):
            count = 10

        count = min(max(count, 1), 100)  # بین 1 و 100

        # فقط ستون‌های لازم رو واکشی کن (نه کل فیلدها)
        qs = cls.objects.only("id", "first_name","last_name","father_name", "national_code","","expired_file_number")

        if query:
            qs = qs.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(national_code__icontains=query) |
                Q(father_name__icontains=query) |
                Q(expired_file_number__icontains=query)
            )

        # در دیتاست‌های بزرگ slicing باعث اجرای مستقیم limit در SQL میشه
        return qs.order_by("-expired_file_number")[:count]
  
    @staticmethod
    def get_enum_key(choices, value):
        """
        تبدیل مقدار فارسی به کلید معادل Enum
        """
        choices_dict = dict(choices)
        # برگرداندن کلید معادل مقدار
        v = str(value).strip()
        for key, val in choices_dict.items():
            vi =  str(val).strip()
            chekced = v == vi
            if chekced:
                return key
        return None  
    
    @classmethod
    def save_record(cls, record):
        try:
            print("[national_code]:",record['national_code'])
            processed = {}
            valid_fields = {f.name for f in cls._meta.get_fields()}

            # --- مرحله‌ی ۱: پاک‌سازی و تبدیل مقادیر ---
            for field, value in record.items():
                # ❌ بررسی نام فیلد معتبر
                if field not in valid_fields:
                    raise ValidationError(f"فیلد نامعتبر در داده ورودی: '{field}'")

                # حذف NaN
                if isinstance(value, float) and math.isnan(value):
                    value = ''
                elif isinstance(value, str):
                    value = value.strip()

                # تبدیل enum فارسی به کلید
                if field == "expired_reason" and value:
                    key = ExpiredSoldier.get_enum_key(EXPIRED_REASON_CHOICES, value)
                    if key:
                        value = key
                    else:
                        value = ExpiredReasonEnum.EXPIRED.value
                # تبدیل تاریخ جلالی به میلادی
                if field in ["start_service_date", "end_service_date", "settlement_date", "runaway_date"]:

                    if value:
                        try:
                            parts = re.split(r"[/\-,.]", str(value))
                            if len(parts) == 3:
                                jy, jm, jd = map(int, parts)
                                value = jdatetime.date(jy, jm, jd).togregorian()
                        except Exception:
                            raise ValidationError(f"تبدیل تاریخ برای {field} ناموفق بود: {value}")

                    if not value:
                        value = None
                        
                processed[field] = value

            # --- مرحله‌ی ۲: ذخیره در دیتابیس ---
            national_code = processed.get("national_code")

            if not national_code:
                raise ValidationError("کد ملی خالی است. ذخیره امکان‌پذیر نیست.")

            # عملیات اتمیک برای جلوگیری از خطاهای همزمانی
            with transaction.atomic():
                expired_soldier, created = ExpiredSoldier.objects.update_or_create(
                    national_code=national_code,
                    defaults=processed
                )

            action = "ایجاد شد" if created else "بروزرسانی شد"
            message = f"✅ رکورد با کد ملی {national_code} با موفقیت {action}."

            # status,message,data,is_updated
            return True,message, expired_soldier, not created

        except ValidationError as ve:
            message = f"❌ خطای اعتبارسنجی: {ve}"
            return False, message,record,ve

        except Exception as e:
            message = f"❌ خطای غیرمنتظره در ذخیره رکورد: {e}"
            return False, message,record,e
