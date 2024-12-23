from django.db import models
from django.utils.timezone import now
from units_apps.models import UnitHistory


class OrganizationalCode(models.Model):
    code_number = models.PositiveIntegerField(unique=True, verbose_name='کد سازمانی')
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')  # فعال یا غیرفعال بودن کد

    def __str__(self):
        return f"Code {self.code_number} - {'Active' if self.is_active else 'Inactive'}"


class Soldier(models.Model):
    # مشخصات شخصی
    organizational_code = models.OneToOneField(
        OrganizationalCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="کد سازمانی"
    )
    national_code = models.CharField(
        max_length=10, unique=True, verbose_name="کد ملی"
    )
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    father_name = models.CharField(max_length=50, verbose_name="نام پدر")
    id_card_code = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="کد پاسداری"
    )
    birth_date = models.DateField(verbose_name="تاریخ تولد")
    birth_place = models.CharField(max_length=100, verbose_name="محل تولد")
    issuance_place = models.CharField(max_length=100, verbose_name="محل صدور")
    marital_status = models.CharField(
        max_length=20,
        choices=[('single', 'مجرد'), ('married', 'متاهل')],
        verbose_name="وضعیت تاهل",
    )
    number_of_children = models.PositiveIntegerField(
        default=0, verbose_name="تعداد اولاد"
    )

    # اطلاعات سلامت
    health_status = models.CharField(max_length=100, verbose_name="وضعیت سلامت")
    health_status_description = models.TextField(
        blank=True, null=True, verbose_name="توضیحات وضعیت سلامت"
    )
    blood_group = models.CharField(
        max_length=3,
        choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                 ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        verbose_name="گروه خون",
    )
    naserin_group_number = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="شماره گروه ناصرین"
    )

    # اطلاعات سکونت
    residence = models.CharField(max_length=200, verbose_name="محل سکونت")
    residence_distance_km = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="کیلومتر"
    )
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
    rank = models.CharField(max_length=50, verbose_name="درجه")
    is_guard_duty = models.BooleanField(default=False, verbose_name="پاسدار وظیفه")
    is_fugitive = models.BooleanField(default=False, verbose_name="فراری")
    fugitive_record = models.PositiveIntegerField(
        default=0, verbose_name="سابقه فرار"
    )
    addiction_record = models.PositiveIntegerField(
        default=0, verbose_name="سابقه اعتیاد"
    )
    education_major = models.CharField(
        max_length=100, verbose_name="رشته تحصیلی"
    )
    referral_person = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="معرف"
    )
    dispatch_date = models.DateField(verbose_name="تاریخ اعزام")
    training_duration = models.PositiveIntegerField(
        verbose_name="مدت آموزش (روز)"
    )
    basic_training_center = models.CharField(
        max_length=100, verbose_name="نام آموزشگاه رزم مقدماتی"
    )
    service_duration_completed = models.PositiveIntegerField(
        verbose_name="مقدار خدمت انجام شده"
    )
    service_entry_date = models.DateField(verbose_name="ورود به یگان")
    total_service_adjustment = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="مجموع (کسری/اضافه خدمت)"
    )
    service_deduction_type = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="نوع کسری خدمت"
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
        choices=[('daily', 'روزانه'), ('weekly', 'هفتگی'), ('monthly', 'ماهانه')],
        verbose_name="تردد",
    )
    essential_service_duration = models.PositiveIntegerField(
        verbose_name="مدت خدمت ضرورت"
    )

    # سایر اطلاعات
    has_driving_license = models.BooleanField(
        default=False, verbose_name="گواهینامه دارد؟"
    )
    driving_license_type = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="نوع گواهینامه"
    )
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
    ideological_training_period = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="دوره عقیدتی"
    )
    independent_married = models.BooleanField(
        default=False, verbose_name="متاهل مستقل"
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
    introduction_letter_scan = models.FileField(
        upload_to='documents/', blank=True, null=True, verbose_name="اسکن معرفی نامه"
    )
    photo_scan = models.ImageField(
        upload_to='photos/', blank=True, null=True, verbose_name="اسکن عکس"
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
        max_length=100, blank=True, null=True, verbose_name="گروه مهارتی"
    )
    skill_certificate = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="مدرک مهارتی"
    )
    number_of_certificates = models.PositiveIntegerField(
        default=0, verbose_name="تعداد مدرک"
    )
    need_certificate = models.BooleanField(
        default=False, verbose_name="نیاز به مدرک"
    )

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

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.organizational_code}"
