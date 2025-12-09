import uuid
import os
from django.db import models
from django.utils.timezone import now
from units_apps.models import UnitHistory
from django.utils.deconstruct import deconstructible
from multiselectfield import MultiSelectField
import re
from datetime import date
from dateutil.relativedelta import relativedelta
from .constants import *
from datetime import date
from almahdiapp.utils.date import gtosh

@deconstructible
class PathAndRename:
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # تولید یک اسم یونیک با uuid
        filename = f"{uuid.uuid4().hex}.{ext}"
        return os.path.join(self.sub_path, filename)


class Soldier(models.Model):
    degree_choices = degree_choices 
    is_guard_duty_CHOICES = is_guard_duty_CHOICES 
    driving_license_type_choices = driving_license_type_choices 
    has_driving_license_choices = has_driving_license_choices 
    skill_group_choices = skill_group_choices 
    independent_married_choices = independent_married_choices
    need_certificate_choices = need_certificate_choices 
    skill_certificate_choices = skill_certificate_choices
    RANK_CHOICES = RANK_CHOICES 
    MARITAL_STATUS_CHOICES = MARITAL_STATUS_CHOICES
    HEALTH_STATUS_CHOICES = HEALTH_STATUS_CHOICES
    blood_group_choices = blood_group_choices
    traffic_status_choices = traffic_status_choices 

   # مشخصات شخصی
    organizational_code = models.ForeignKey(
        'OrganizationalCode',   # مدل مرتبط
        on_delete=models.SET_NULL,  # اگر کد حذف شد، فیلد null شود
        null=True,
        blank=True,
        verbose_name="کد سازمانی",
        related_name="soldiers"  # حالا می‌توان به همه سربازان یک کد دسترسی داشت
    )
    
    @property
    def organizational_code_display(self):
        if not self.organizational_code:
            return None
        
        return self.organizational_code.code_number
    
    @property
    def is_active_code(self):
        """
        بررسی می‌کند که آیا این سرباز فعلی برای کد سازمانی است یا نه
        """
        if not self.organizational_code:
            return False  # سرباز کد ندارد

        current_soldier = getattr(self.organizational_code, 'current_soldier', None)
        return current_soldier is not None and current_soldier.id == self.id

    
    national_code = models.CharField(
        max_length=10, unique=True, verbose_name="کد ملی"
    )
    first_name = models.CharField(max_length=100, verbose_name="نام", null=True, blank=True)
    last_name = models.CharField(max_length=150, verbose_name="نام خانوادگی", null=True, blank=True)
    father_name = models.CharField(max_length=150, verbose_name="نام پدر", null=True, blank=True)
    id_card_code = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="کد پاسداری"
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    birth_place = models.CharField(max_length=100, verbose_name="محل تولد", null=True, blank=True)
    issuance_place = models.CharField(max_length=100, verbose_name="محل صدور", null=True, blank=True)
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        verbose_name="وضعیت تاهل",
        null=True,
        blank=True,
    )
    
    number_of_children = models.PositiveIntegerField(
        default=0, verbose_name="تعداد اولاد"
    )

    # اطلاعات سلامت
    health_status = models.CharField(
        max_length=100,
        choices=HEALTH_STATUS_CHOICES,
        verbose_name="وضعیت سلامت", null=True, blank=True,
    )
    health_status_description = models.TextField(
        blank=True, null=True, verbose_name="توضیحات وضعیت سلامت"
    )
    
    blood_group = models.CharField(
        max_length=3,
        choices=blood_group_choices,
        verbose_name="گروه خون",
        null=True,
        blank=True,
    )
    naserin_group = models.ForeignKey(
        'soldire_naserin_apps.NaserinGroup', on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name="گروه ناصرین"
    )

    # اطلاعات سکونت
    residence_city = models.ForeignKey('cities_iran_manager_apps.City', on_delete=models.SET_NULL, null=True,
                                       blank=True, verbose_name='شهر')
    residence_province = models.ForeignKey('cities_iran_manager_apps.Province', on_delete=models.SET_NULL, null=True,
                                           blank=True, verbose_name='استان')
    postal_code = models.CharField(max_length=10, verbose_name="کدپستی")
    phone_home = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="منزل"
    )
    phone_mobile = models.CharField(max_length=15, verbose_name="موبایل")
    phone_virtual = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="همراه مجازی"
    )
    phone_parents = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="همراه پدر یا مادر"
    )

    # اطلاعات نظامی
    rank = models.CharField(
        choices=RANK_CHOICES,
        max_length=50,
        verbose_name="درجه",
        blank=True,
        null=True,

    )
    is_guard_duty = models.BooleanField(default=False, verbose_name="پاسدار وظیفه")
    is_fugitive = models.BooleanField(default=False, verbose_name="فراری")
    fugitive_record = models.PositiveIntegerField(
        default=0, verbose_name="سابقه فرار", null=True, blank=True
    )
    addiction_record = models.PositiveIntegerField(
        default=0, verbose_name="سابقه اعتیاد", blank=True, null=True,
    )
    referral_person = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="معرف"
    )
    dispatch_date = models.DateField(null=True, blank=True, verbose_name='تاریخ اعزام')
    training_duration = models.PositiveIntegerField(
        verbose_name="مدت آموزش (روز)"
    )
    basic_training_center = models.ForeignKey('training_center_apps.TrainingCenter', on_delete=models.CASCADE,
                                              verbose_name='نام آموزشگاه رزم مقدماتی', blank=True, null=True)
    service_duration_completed = models.PositiveIntegerField(
        verbose_name="مقدار خدمت انجام شده", blank=True, null=True,
    )

    service_entry_date = models.DateField(null=True, blank=True, verbose_name='تاریخ ورود به یگان')

    total_service_adjustment = models.IntegerField(verbose_name="مجموع (کسری/اضافه خدمت)", null=True, blank=True)
    service_deduction_type = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="نوع کسری خدمت"
    )
    service_extension_type = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="نوع اضافه خدمت"
    )
    service_end_date = models.DateField(
        blank=True, null=True, verbose_name="پایان خدمت"
    )
    @property
    def service_end_date_display(self):
        if self.service_end_date:
            return gtosh(self.service_end_date)
        return "-"


    @property
    def remaining_days(self):
        """تعداد روز باقی مانده خدمت"""
        if self.service_end_date:
            delta = self.service_end_date - date.today()
            return max(delta.days, 0)  # منفی نباشد
        return None

    @property
    def remaining_years_months_days(self):
        """تعداد سال، ماه و روز باقی مانده"""
        if self.service_end_date:
            today = date.today()
            if self.service_end_date < today:
                return (0, 0, 0)
            delta = relativedelta(self.service_end_date, today)
            return delta.years, delta.months, delta.days
        return (0, 0, 0)

    @property
    def remaining_str(self):
        """رشته باقی مانده خدمت"""
        y, m, d = self.remaining_years_months_days
        days = self.remaining_days

        if days is None:
            return "نامشخص"
        parts = []
        if y > 0:
            parts.append(f"{y} سال")
        if m > 0:
            parts.append(f"{m} ماه")
        if d > 0:
            parts.append(f"{d} روز")
        if not parts:
            return "اتمام خدمت"
        return " و ".join(parts)
    # اطلاعات محل خدمت
    @property
    def remaining_str_type(self):
        days = self.remaining_days
        if days is None:
            return "unknown"
        elif days == 0:
            return "end"
        elif days <= 15:
            return "remaining15"
        elif days <= 30:
            return "remaining30"
        elif  days <= 45:
            return "remaining45"
        
    @classmethod
    def date_to_ends(cls, days: int):
        """
        فهرست سربازانی که بین 0 تا days روز تا پایان خدمت مانده‌اند
        """
        from datetime import date, timedelta

        today = date.today()
        max_date = today + timedelta(days=days)

        # سربازانی که تاریخ پایانشان بین امروز تا روز هدف است
        return cls.objects.filter(service_end_date__range=(today, max_date))

    current_parent_unit = models.ForeignKey(
        "units_apps.ParentUnit", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="واحد اصلی فعلی"
    )
    current_sub_unit = models.ForeignKey(
        "units_apps.SubUnit", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="زیرواحد فعلی"
    )

    traffic_status = models.CharField(
        max_length=50,
        choices=traffic_status_choices,
        verbose_name="تردد",
        blank=True,
        null=True,
    )
    essential_service_duration = models.PositiveIntegerField(
        verbose_name="مدت خدمت ضرورت"
    )

    # سایر اطلاعات
    has_driving_license = models.CharField(
        max_length=200, verbose_name="گواهینامه دارد؟", null=True, blank=True,
        choices=has_driving_license_choices
    )

    driving_license_type = MultiSelectField(choices=driving_license_type_choices, max_length=200, null=True, blank=True,
                                            verbose_name='نوع گواهینامه')

    file_shortage = models.TextField(
        blank=True, null=True, verbose_name="کسری پرونده"
    )
    comments = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    address = models.TextField(verbose_name="آدرس منزل")
    saman_username = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="نام کاربری ثامن"
    )
    card_chip = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="تراشه/کارت"
    )
    ideological_training_period = models.ForeignKey('soldire_religious_period_apps.ReligiousPeriod',
                                                    on_delete=models.SET_NULL, null=True, blank=True,
                                                    verbose_name="دوره عقیدتی",
                                                    related_name='training_period_ideological'
                                                    )
    independent_married = models.BooleanField(
        default=False, verbose_name="متاهل مستقل", null=True, blank=True,
    )
    weekly_or_monthly_presence = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="حضور هفتگی/ماهانه"
    )
    is_needy = models.BooleanField(default=False, verbose_name="معسرین")
    expertise = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="تخصص"
    )
    is_sunni = models.BooleanField(default=False, verbose_name="اهل تسنن")
    is_sayyed = models.BooleanField(default=False, verbose_name="سید")

    photo_scan = models.ImageField(
        upload_to=PathAndRename('photos/'),
        blank=True,
        null=True,
        verbose_name="اسکن عکس"
    )
    eligible_for_card_issuance = models.BooleanField(
        default=True, verbose_name="واجد شرایط صدور کارت پایان خدمت"
    )
    card_issuance_status = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="وضعیت صدور کارت پایان خدمت"
    )
    expired_file_number = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="شماره پرونده منقضی خدمت"
    )
    skill_5 = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="مهارت 5گانه"
    )
    skill_group = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="گروه مهارتی", choices=skill_group_choices
    )
    skill_certificate = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="مدرک مهارتی", choices=skill_certificate_choices
    )
    number_of_certificates = models.PositiveIntegerField(
        default=0, verbose_name="تعداد مدرک", null=True, blank=True,
    )
    is_certificate = models.BooleanField(
        default=False, verbose_name="مدرک مهارت آموزی دارد؟", choices=need_certificate_choices, null=True, blank=True
    )
    is_top5 = models.BooleanField(
        default=False, verbose_name="برتر", choices=need_certificate_choices, null=True, blank=True
    )
    degree = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="مدرک تحصیلی", choices=degree_choices
    )
    field_of_study = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="رشته تحصیلی"
    )
    system_presence = models.BooleanField(null=True,blank=True,default=True,verbose_name="اعلام حضور سامانه")
    absorption = models.BooleanField(default=False, verbose_name='جذبی؟')
    Is_the_Basij_sufficient = models.BooleanField(default=False, verbose_name='کفایتدار بسیج')
    height = models.CharField(max_length=200, null=True, blank=True, verbose_name='قد')
    weight = models.CharField(max_length=200, null=True, blank=True, verbose_name='وزن')
    eye_color = models.CharField(max_length=200, null=True, blank=True, verbose_name='رنگ چشم')
    hair_color = models.CharField(max_length=200, null=True, blank=True, verbose_name='رنگ مو')
    
    STATUS_CHOICES = [
        ('توجیحی', 'توجیحی'),
        ('حین خدمت', 'حین خدمت'),
        ('پایان خدمت', 'پایان خدمت'),
        ('انتقالی', 'انتقالی'),
        ('قبولی در دانشگاه', 'قبولی در دانشگاه'),
        ('استخدام در نیروهای مسلح', 'استخدام در نیروهای مسلح'),
    ]
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, null=True, blank=True, verbose_name='وضعیت فرد')
    is_checked_out = models.BooleanField(default=False, verbose_name='تسویه حساب')

    IMPORTANT_FIELDS = [
        'first_name',
        'last_name',
        'national_code',
        'father_name',
        'birth_date',
        'marital_status',
        'id_card_code',
    ]
    position = models.ForeignKey(
        'organizational_position.OrganizationalPosition',  # ارجاع به مدلی که پایین‌تر تعریف می‌کنیم (string ok)
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='soldiers',
        verbose_name="جایگاه سازمانی"
    )
    position_at = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ انتصاب به جایگاه"
    )
    # 
    @property 
    def clearance_expired_file_number(self):
        from soldire_letter_apps.models import ClearanceLetter
        letter = ClearanceLetter.objects.filter(soldier=self).order_by('-created_at').first()
        if letter  and letter.expired_file_number:
            return letter.expired_file_number
        
        return ''
    
    def get_missing_fields(self):
        missing = []
        for field_name in self.IMPORTANT_FIELDS:
            value = getattr(self, field_name)
            if not value:
                verbose = self._meta.get_field(field_name).verbose_name
                missing.append(verbose)
        return missing


    @property
    def is_entry(self):
        if not self.organizational_code:
            return False
        
        return not self.organizational_code.code_number % 2

    @property
    def is_delay(self):
        if not self.organizational_code:
            return False
        
        return  self.organizational_code.code_number % 3

    @property
    def is_exit(self):
        if not self.organizational_code:
            return False
        
        return self.organizational_code.code_number % 2



        
    def update_has_driving_license(self):
        if self.driving_license_type != "ندارد":
            self.has_driving_license = 'دارد'
        else:
            self.has_driving_license = 'ندارد'

    def update_is_seyed(self):
        full = f"{self.first_name or ''} {self.last_name or ''}"
        self.is_sayyed = "سید" in full
        
    def update_absorption(self):
        if self.referral_person is not None:
            self.absorption = True
        else:
            self.absorption = False

    def change_unit(self, new_parent_unit, new_sub_unit):
        # پایان دادن به واحد قبلی
        last_history = self.unit_history.filter(end_date__isnull=True).last()
        if last_history:
            last_history.end_date = now()
            last_history.save()

        # اضافه کردن واحد جدید به تاریخچه
        UnitHistory.objects.create(
            soldier=self,
            parent_unit=new_parent_unit,
            sub_unit=new_sub_unit,
            start_date=now(),
        )

        # به‌روزرسانی واحد فعلی
        self.current_parent_unit = new_parent_unit
        self.current_sub_unit = new_sub_unit
        self.save()

    def save(self, *args, **kwargs):
        self.update_has_driving_license()
        self.update_is_seyed()
        self.update_absorption()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.organizational_code}"

    
    @classmethod
    def create_minimal_from_import(cls,
        national_code: str,
        first_name: str = '',
        last_name: str = '',
        degree_number=None,
        expired_file_number: str = None,
        defaults: dict = None,
        finished_at=None
    ):
        """
        ایجاد (یا برگرداندن موجود) یک سرباز با اطلاعات حداقلی.
        از national_code به عنوان شناسه اصلی استفاده می‌شود.
        ورودی‌ها:
            - national_code (str): الزامی
            - first_name, last_name (str): اگر موجود نیست، رشته خالی
            - degree_number: عدد یا رشته عددی (1..12)
            - expired_file_number: شماره پرونده منقضی (اختیاری) — در فیلد expired_file_number ذخیره می‌شود
            - defaults: دیکشنری برای override مقادیر پیش‌فرض (مثلاً phone_mobile, postal_code, training_duration ...)
        خروجی: (soldier_instance, created_bool, error_message_or_None)
        """
        from django.db import transaction
        from .utils import map_rank_number_to_choice
        
        if not national_code:
            return None, False, "کد ملی ارسال نشده است."

        defaults = defaults or {}

        # مقادیر پیش‌فرض برای فیلدهای NOT NULL که در مدل شما الزامی هستند
        safe_defaults = {
            "phone_mobile": defaults.get("phone_mobile", "0000000000"),
            "postal_code": defaults.get("postal_code", ""),
            "training_duration": defaults.get("training_duration", 0),
            "address": defaults.get("address", ""),
            "essential_service_duration": defaults.get("essential_service_duration", 0),
            # اگر مدل فیلدهای دیگری اجباری دارد، اینجا اضافه کنید
        }

        # نگاشت درجه عددی به مقدار choices
        rank_choice = map_rank_number_to_choice(degree_number)

        try:
            with transaction.atomic():
                soldier, created = cls.objects.get_or_create(
                    national_code=str(national_code).strip(),
                    defaults={
                        "first_name": first_name or "",
                        "last_name": last_name or "",
                        "rank": rank_choice,
                        # فیلدهای اجباری را از safe_defaults پر کن
                        "phone_mobile": safe_defaults["phone_mobile"],
                        "postal_code": safe_defaults["postal_code"],
                        "training_duration": safe_defaults["training_duration"],
                        "address": safe_defaults["address"],
                        "essential_service_duration": safe_defaults["essential_service_duration"],
                        # وضعیت تسویه را فعال کن چون گفته بودی تسویه حساب شده
                        "is_checked_out": True,
                        "service_end_date":finished_at,
                        # اگر نیاز داری فیلد وضعیت را هم ست کنی می‌توانی:
                        # "status": "پایان خدمت",
                    }
                )
                # اگر قبلاً موجود بوده، ممکن است بخواهی بعضی فیلدهای حداقلی را همین‌جا آپدیت کنی
                if not created:
                    changed = False
                    if first_name and not soldier.first_name:
                        soldier.first_name = first_name
                        changed = True
                    if last_name and not soldier.last_name:
                        soldier.last_name = last_name
                        changed = True
                    if rank_choice and not soldier.rank:
                        soldier.rank = rank_choice
                        changed = True
                    if expired_file_number and not soldier.expired_file_number:
                        soldier.expired_file_number = expired_file_number
                        changed = True
                    # اگر می‌خواهی حتماً is_checked_out را ست کنی:
                    if not soldier.is_checked_out:
                        soldier.is_checked_out = True
                        changed = True

                    if changed:
                        soldier.save()

                else:
                    # رکورد جدید؛ مقدار expired_file_number را تنظیم کن اگر ارسال شده
                    if expired_file_number:
                        soldier.expired_file_number = expired_file_number
                        soldier.save(update_fields=["expired_file_number"])

                return soldier, created, None

        except Exception as e:
            return None, False, str(e)

    def to_checkout(self):
        # 1️⃣ علامت‌گذاری خروج سرباز
        self.is_checked_out = True
        self.save(update_fields=['is_checked_out'])

        # 2️⃣ پیدا کردن کد سازمانی که این سرباز در آن است
        orgc = self.organizational_code
        # 3️⃣ بررسی کد ملی و آزاد کردن کد سازمانی
        if orgc and orgc.current_soldier and  self.national_code == orgc.current_soldier.national_code:
            orgc.current_soldier = None
            orgc.save(update_fields=['current_soldier'])
    @property
    def organizational_code_display_letter(self):
        """
        ایجاد متن ترکیبی برای نمایش در نامه بر اساس:
        - کد سازمانی
        - شماره پرونده منقضی
        - وضعیت تسویه

        هر موردی که وجود نداشته باشد از متن حذف می‌شود.
        """

        parts = []

        # کد سازمانی
        if getattr(self, "organizational_code", None):
            parts.append(f"کد سازمانی: {self.organizational_code.code_number}")

        # وضعیت تسویه
        if getattr(self, "is_checked_out", None):
            parts.append(f"شماره پرونده منقضی: {self.expired_file_number}")
            parts.append(f"وضعیت تسویه: {self.clearance_status}")

        # اگر هیچ مقداری نبود
        if len(parts) < 1:
            return "اطلاعات سازمانی ثبت نشده است"

        # ترکیب نهایی
        return " ، ".join(parts)

         
class OrganizationalCode(models.Model):
    code_number = models.PositiveIntegerField(unique=True, verbose_name='کد سازمانی')
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')  # فعال یا غیرفعال بودن کد
    current_soldier = models.OneToOneField(
        'Soldier',                 # مدل مرتبط
        on_delete=models.SET_NULL,  # اگر سرباز حذف شد، فیلد null شود
        null=True,
        blank=True,
        related_name='current_code',
        verbose_name='سرباز فعلی'
    )
    
        
    def __str__(self):
        active_label = 'آزاد'
        if  self.is_active or self.current_soldier:
            active_label = 'غیر آزاد'
            
        
        return f"کد سازمانی : {self.code_number} - {active_label}"


class Settlement(models.Model):
    soldier = models.OneToOneField("Soldier", on_delete=models.CASCADE, related_name="settlement")

    reason_for_non_issuance = models.TextField("علت عدم صدور", blank=True, null=True)

    total_debt_rial = models.BigIntegerField("میزان بدهی (ریال)", default=0)
    current_debt_rial = models.BigIntegerField("بدهی باقی‌مانده (ریال)", default=0)

    last_rights_check_date = models.DateField("اخرین تاریخ بررسی حقوق", blank=True, null=True)
    need_rights_recheck = models.BooleanField("نیاز به بررسی مجدد حقوق", default=True)

    final_settlement_date = models.DateField("تاریخ ثبت تسویه در سامانه", blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('review', 'بررسی حقوق'),
            ('pending', 'در انتظار تسویه'),
            ('partial', 'تسویه ناقص'),
            ('cleared', 'تسویه کامل'),
            ('transferred', 'انتقالی'),
        ],
        default='review',
        verbose_name="وضعیت"
    )

    description = models.TextField("توضیحات", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_debt_status(self):
        total_paid = sum(payment.amount_rial for payment in self.payments.all())

        # اگر پرداخت بیش از کل بدهی باشه، باز هم بدهی صفر میشه ولی وضعیت باید دقیق مشخص بشه
        self.current_debt_rial = max(self.total_debt_rial - total_paid, 0)

        if total_paid >= self.total_debt_rial:
            self.status = 'cleared'
        elif total_paid > 0:
            self.status = 'partial'
        else:
            self.status = 'pending'

        self.save()

    def __str__(self):
        return f"تسویه - {self.soldier}"

class PaymentReceipt(models.Model):
    settlement = models.ForeignKey(Settlement, on_delete=models.CASCADE, related_name="payments")

    amount_rial = models.BigIntegerField("مبلغ واریزی (ریال)")
    receipt_number = models.CharField("شماره فیش واریزی", max_length=100)
    deposit_date = models.CharField(max_length=120,verbose_name="تاریخ فیش واریزی")
    bank_operator_code = models.CharField("کد متصدی بانک", max_length=50)

    receipt_file = models.FileField("فایل فیش", upload_to='receipts/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.settlement.update_debt_status()

    def __str__(self):
        return f"{self.receipt_number} - {self.amount_rial} ریال"



