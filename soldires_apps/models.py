import uuid
import os
from django.db import models
from django.utils.timezone import now
from units_apps.models import UnitHistory
from training_center_apps.models import TrainingCenter
from django_jalali.db import models as jmodels
from django.utils.deconstruct import deconstructible
from multiselectfield import MultiSelectField
import re
from django.utils import timezone


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
    degree_choices = [
        ('زیردیپلم', 'زیردیپلم'),
        ('دیپلم', 'دیپلم'),
        ('فوق دیپلم', 'فوق دیپلم'),
        ('لیسانس', 'لیسانس'),
        ('فوق لیسانس', 'فوق لیسانس'),
        ('دکترا', 'دکترا'),
        ('دکترا پزشکی', 'دکترا پزشکی'),
    ]
    is_guard_duty_CHOICES = [
        (False, 'خیر'),
        (True, 'بلی'),
    ]
    driving_license_type_choices = [
        ('پایه سوم', 'پایه سوم'),
        ('پایه دوم', 'پایه دوم'),
        ('پایه اول', 'پایه اول'),
        ('موتورسیکلت', 'موتورسیکلت'),
        ('ویژه', 'ویژه'),
        ('ندارد', 'ندارد'),
    ]
    has_driving_license_choices = [
        ('دارد', 'دارد'),
        ('ندارد', 'ندارد'),
    ]
    skill_group_choices = [
        (
            'گروه 1 : پزشکی و پیراپزشکی = گروه پیراپزشکی(رادیولوژی،هوش بری،علوم آزمایشگاهی،اتاق عمل،فوریت پزشکی ،کادر درمان)',
            'گروه 1 : پزشکی و پیراپزشکی = گروه پیراپزشکی(رادیولوژی،هوش بری،علوم آزمایشگاهی،اتاق عمل،فوریت پزشکی ،کادر درمان)'),
        ('گروه 2 : تحصیلات تکمیلی و غیرپزشکی = فوق لیسانس، دکتری و فوق دکتری',
         'گروه 2 : تحصیلات تکمیلی و غیرپزشکی = فوق لیسانس، دکتری و فوق دکتری'),
        ('گروه 3 : لیسانس = در صورت بکارگیری در پست مرتبط با تحصیلات ،عدم نیاز به آموزش',
         'گروه 3 : لیسانس = در صورت بکارگیری در پست مرتبط با تحصیلات ،عدم نیاز به آموزش'),
        ('گروه 4 : فوق دیپلم و دیپلم فنی و حرفه ای و کاردانش', 'گروه 4 : فوق دیپلم و دیپلم فنی و حرفه ای و کاردانش'),
        ('گروه 5 : فوق دیپلم و دیپلم به پایین', 'گروه 5 : فوق دیپلم و دیپلم به پایین'),
        ('گروه 6 : دارندگان گواهینامه فنی و حرفه ای', 'گروه 6 : دارندگان گواهینامه فنی و حرفه ای'),
        ('گروه 7 : فوق دیپلم و دیپلم که در سالهای گذشته گواهینامه گرفته اند و همچنان سرباز می باشند',
         'گروه 7 : فوق دیپلم و دیپلم که در سالهای گذشته گواهینامه گرفته اند و همچنان سرباز می باشند')
    ]
    independent_married_choices = [
        (True, 'بله'),
        (False, 'خیر')
    ]
    need_certificate_choices = [
        (True, 'بله'),
        (False, 'خیر')
    ]
    skill_certificate_choices = [
        ('مدرک 1', 'مدرک 1')
    ]
    RANK_CHOICES = [
        ('سرباز(1)', 'سرباز(1)'),
        ('سرباز دوم(2)', 'سرباز دوم(2)'),
        ('سرباز یکم(3)', 'سرباز یکم(3)'),
        ('رزمیار(4)', 'رزمیار(4)'),
        ('رزم آور سوم(5)', 'رزم آور سوم(5)'),
        ('رزم آور دوم(6)', 'رزم آور دوم(6)'),
        ('رزم آور یکم(7)', 'رزم آور یکم(7)'),
        ('رزمدار دوم(8)', 'رزمدار دوم(8)'),
        ('رزمدار یکم(9)', 'رزمدار یکم(9)'),
        ('ستوان سوم(10)', 'ستوان سوم(10)'),
        ('ستوان دوم(11)', 'ستوان دوم(11)'),
        ('ستوان یکم(12)', 'ستوان یکم(12)'),

    ]
    MARITAL_STATUS_CHOICES = [('مجرد', 'مجرد'), ('متاهل', 'متاهل')]
    HEALTH_STATUS_CHOICES = [('سالم', 'سالم'), ('معاف از رزم', 'معاف از رزم'), ('گروه ب', 'گروه ب'),
                             ('معاف+گروه ب', 'معاف+گروه ب'), ]
    blood_group_choices = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                           ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')]
    traffic_status_choices = [('روزانه', 'روزانه'), ('هفتگی', 'هفتگی'), ('ماهانه', 'ماهانه')]
    # مشخصات شخصی
    organizational_code = models.OneToOneField(
        'OrganizationalCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="کد سازمانی"
    )
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
    # اطلاعات محل خدمت
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
    degree = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="مدرک تحصیلی", choices=degree_choices
    )
    field_of_study = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="رشته تحصیلی"
    )
    absorption = models.BooleanField(default=False, verbose_name='جذبی؟')
    Is_the_Basij_sufficient = models.BooleanField(default=False, verbose_name='کفایتدار بسیج')

    IMPORTANT_FIELDS = [
        'first_name',
        'last_name',
        'national_code',
        'father_name',
        'birth_date',
        'marital_status',
        'id_card_code',
    ]

    def get_missing_fields(self):
        missing = []
        for field_name in self.IMPORTANT_FIELDS:
            value = getattr(self, field_name)
            if not value:
                verbose = self._meta.get_field(field_name).verbose_name
                missing.append(verbose)
        return missing

    def update_has_driving_license(self):
        if self.driving_license_type != "ندارد":
            self.has_driving_license = 'دارد'
        else:
            self.has_driving_license = 'ندارد'

    def update_is_seyed(self):
        if re.search(r'(^|[\s‌])سید', self.first_name):
            self.is_sayyed = True
        else:
            self.is_sayyed = False

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


class OrganizationalCode(models.Model):
    code_number = models.PositiveIntegerField(unique=True, verbose_name='کد سازمانی')
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')  # فعال یا غیرفعال بودن کد

    def __str__(self):
        return f"کد {self.code_number} - {'غیرآزاد' if self.is_active else 'آزاد'}"


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
            ('pending', 'در انتظار تسویه'),
            ('partial', 'تسویه ناقص'),
            ('cleared', 'تسویه کامل'),
            ('transitional', 'انتقالی'),
            ('review', 'بررسی'),
        ],
        default='pending',
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
    deposit_date = models.DateField("تاریخ فیش واریزی")
    bank_operator_code = models.CharField("کد متصدی بانک", max_length=50)

    receipt_file = models.FileField("فایل فیش", upload_to='receipts/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.settlement.update_debt_status()

    def __str__(self):
        return f"{self.receipt_number} - {self.amount_rial} ریال"
