from django import forms
from .models import Soldier, OrganizationalCode
from training_center_apps.models import TrainingCenter
from units_apps.models import ParentUnit, SubUnit
from cities_iran_manager_apps.models import City, Province


class SoldierForm(forms.ModelForm):
    residence_province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        empty_label="انتخاب استان",
        widget=forms.Select(attrs={"class": "form-control", "id": "province-select"}),
        label='استان'
    )

    residence_city = forms.ModelChoiceField(
        queryset=City.objects.none(),  # ابتدا خالی می‌گذاریم تا با AJAX پر شود
        empty_label="انتخاب شهر",
        widget=forms.Select(attrs={"class": "form-control", "id": "city-select"}),
        label='شهر',
    )
    organizational_code = forms.ModelChoiceField(
        queryset=OrganizationalCode.objects.filter(is_active=False).all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='کدسازمانی',
    )

    rank = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.RANK_CHOICES,  # اگر در مدل Soldier مقدار choices تعریف شده
        label='درجه',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    current_parent_unit = forms.ModelChoiceField(
        queryset=ParentUnit.objects.all(),
        empty_label="انتخاب واحد اصلی",
        widget=forms.Select(attrs={"class": "form-control", "id": "parent-unit-select"}),
        label='قسمت', required=False,
    )

    current_sub_unit = forms.ModelChoiceField(
        queryset=SubUnit.objects.none(),  # مقدار اولیه خالی، بعداً با AJAX پر می‌شود
        empty_label="انتخاب زیرواحد",
        widget=forms.Select(attrs={"class": "form-control", "id": "sub-unit-select"}),
        label='زیرقسمت',
        required=False,
    )

    basic_training_center = forms.ModelChoiceField(
        queryset=TrainingCenter.objects.all(),  # فرض بر این است که مراکز آموزشی در این مدل ذخیره شده‌اند
        empty_label="انتخاب کنید...",
        label='نام آموزشگاه رزم مقدماتی',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    marital_status = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.MARITAL_STATUS_CHOICES,  # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='وضعیت تأهل',
        required=False,
    )

    health_status = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.HEALTH_STATUS_CHOICES,  # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='وضعیت سلامت',
        required=False
    )
    is_guard_duty = forms.ChoiceField(
        choices=Soldier.is_guard_duty_CHOICES,  # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='پاسدار وظیفه',
        required=False,

    )
    is_certificate = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.need_certificate_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='مدرک مهارت آموزی دارد؟',
        required=False,
    )
    skill_certificate = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.skill_certificate_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='نوع مدرک مهارتی',
        required=False,
    )
    independent_married = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.independent_married_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='متاهل مستقل',
        required=False,
    )
    skill_group = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.skill_group_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='گروه مهارتی',
        required=False,
    )
    blood_group = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.blood_group_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='گروه خون',
        required=False,
    )
    birth_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تاریخ تولد را وارد کنید'}),
        label='تاریخ تولد',
    )
    dispatch_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تاریخ اعزام را وارد کنید'}),
        label='تاریخ اعزام',
    )
    service_entry_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تاریخ ورود به یگان را وارد کنید'}),
        label='تاریخ ورود به یگان',
    )

    degree = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.degree_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='مدرک تحصیلی',
        required=False,
    )
    traffic_status = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.traffic_status_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='تردد',
        required=False,
    )
    is_sunni = forms.BooleanField(
        required=False,  # به صورت پیش‌فرض مقدار True یا False می‌گیرد
        label="اهل تسنن؟",  # اضافه کردن برچسب
        initial=False  # مقدار پیش‌فرض False است
    )
    is_needy = forms.BooleanField(
        required=False,  # به صورت پیش‌فرض مقدار True یا False می‌گیرد
        label="معسرین؟",  # اضافه کردن برچسب
        initial=False  # مقدار پیش‌فرض False است
    )
    Is_the_Basij_sufficient = forms.BooleanField(
        required=False,  # به صورت پیش‌فرض مقدار True یا False می‌گیرد
        label="کفایتدار بسیج؟",  # اضافه کردن برچسب
        initial=False  # مقدار پیش‌فرض False است
    )

    class Meta:
        model = Soldier
        fields = '__all__'
        widgets = {
            # ۱. اطلاعات هویتی و شناسایی
            'national_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کدملی را وارد کنید'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام را وارد کنید'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی را وارد کنید'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام پدر را وارد کنید'}),
            'birth_place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'محل تولد را وارد کنید'}),
            'issuance_place': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'محل صدور شناسنامه را وارد کنید'}),

            # ۲. اطلاعات تماس و محل سکونت
            'address': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'آدرس منزل را وارد کنید', 'rows': '3'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کدپستی را وارد کنید'}),
            'phone_mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'موبایل را وارد کنید'}),
            'phone_virtual': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'همراه مجازی را وارد کنید'}),
            'phone_parents': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'همراه پدر یا مادر را وارد کنید'}),
            'phone_home': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'منزل را وارد کنید'}),

            # ۳. اطلاعات سازمانی و خدمتی
            'id_card_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد پاسداری را وارد کنید'}),
            'saman_username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'نام کاربری ثامن را وارد کنید'}),
            'card_chip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تراشه/کارت را وارد کنید'}),
            # ۴. وضعیت خدمتی و سوابق
            'training_duration': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'مدت آموزش (روز) را وارد کنید'}),
            'service_duration_completed': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'مقدار خدمت انجام شده را وارد کنید'}),
            'essential_service_duration': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'مدت خدمت ضرورت را وارد کنید'}),
            # ۵. وضعیت خانوادگی و اجتماعی
            'number_of_children': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'تعداد اولاد را وارد کنید'}),
            # ۶. وضعیت سلامت و مدارک پزشکی
            'health_status_description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'توضیحات وضعیت سلامت را وارد کنید'}),
            # ۷. مهارت‌ها و سوابق آموزشی
            'is_needy': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'معسرین را وارد کنید'}),
            'number_of_certificates': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'تعداد را وارد کنید'}),
            # ۹. اطلاعات بسیج و عقیدتی
            # ۱۰. اطلاعات مرتبط با مدارک و استعلامات
            'field_of_study': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'توضیحات رشته تحصیلی را وارد کنید'}),
            'expertise': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'توضیحات تخصص را وارد کنید'}),
            'driving_license_type': forms.CheckboxSelectMultiple(),
            'referral_person': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'معرف را وارد کنید'}),
        }

        def clean_national_code(self):
            national_code = self.cleaned_data.get('national_code')
            # اینجا می‌توانید شرط‌های خود را اعمال کنید
            find_soldire = Soldier.objects.filter(national_code=national_code).filter()
            if find_soldire is not None:
                raise forms.ValidationError("سرباز با این کدملی موجود دارد.")
            if national_code and len(national_code) != 10:
                raise forms.ValidationError("کد ملی باید دقیقاً ۱۰ رقم باشد.")
            return national_code

        def clean_is_guard_duty(self):
            is_guard_duty = self.cleaned_data.get('is_guard_duty')
            if is_guard_duty == "بلی":
                return True
            if is_guard_duty == "خیر":
                return False

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['organizational_code'].queryset = Soldier.objects.filter(status='آزاد')
            self.fields['organizational_code'].empty_label = OrganizationalCode.objects.filter(is_active=False).first()
            if "province" in self.data:
                try:
                    province_id = int(self.data.get("province"))
                    self.fields["city"].queryset = City.objects.filter(province_id=province_id)
                except (ValueError, TypeError):
                    pass
            if "parent_unit" in self.data:
                try:
                    parent_unit_id = int(self.data.get("parent_unit"))
                    self.fields["sub_unit"].queryset = SubUnit.objects.filter(parent_unit_id=parent_unit_id)
                except (ValueError, TypeError):
                    pass


class SoldierSearchForm(forms.Form):
    # اطلاعات هویتی
    national_code = forms.CharField(label='کد ملی', required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='نام', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='نام خانوادگی', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    father_name = forms.CharField(label='نام پدر', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    organizational_code = forms.CharField(label='کد سازمانی', required=False,
                                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    id_card_code = forms.CharField(label='کد پاسداری', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    # اطلاعات مکانی
    birth_place = forms.CharField(label='محل تولد', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    issuance_place = forms.CharField(label='محل صدور', required=False,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    residence_province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        label='استان',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    residence_city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label='شهر',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # اطلاعات خدمت
    current_parent_unit = forms.ModelChoiceField(
        queryset=ParentUnit.objects.all(),
        label='قسمت',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    current_sub_unit = forms.ModelChoiceField(
        queryset=SubUnit.objects.all(),
        label='زیرقسمت',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    rank = forms.ChoiceField(
        choices=Soldier.RANK_CHOICES,
        label='درجه',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_guard_duty = forms.BooleanField(
        label='پاسدار وظیفه',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # اطلاعات زمانی
    service_entry_date = forms.CharField(
        label='تاریخ ورود به یگان',
        required=False,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
    )
    dispatch_date = forms.CharField(
        label='تاریخ اعزام',
        required=False,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
    )
    birth_date = forms.CharField(
        label='تاریخ تولد',
        required=False,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
    )

    # اطلاعات آموزشی
    training_duration = forms.IntegerField(
        label='مدت آموزش (روز)',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    basic_training_center = forms.ModelChoiceField(
        queryset=TrainingCenter.objects.all(),
        label='نام آموزشگاه رزم مقدماتی',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    essential_service_duration = forms.IntegerField(
        label='مدت خدمت ضرورت',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    # اطلاعات شخصی
    marital_status = forms.ChoiceField(
        choices=Soldier.MARITAL_STATUS_CHOICES,
        label='وضعیت تأهل',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    independent_married = forms.BooleanField(
        label='متاهل مستقل',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    number_of_children = forms.IntegerField(
        label='تعداد اولاد',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    # اطلاعات سلامت
    health_status = forms.ChoiceField(
        choices=Soldier.HEALTH_STATUS_CHOICES,
        label='وضعیت سلامت',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    health_status_description = forms.CharField(
        label='توضیحات وضعیت سلامت',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    blood_group = forms.ChoiceField(
        choices=Soldier.blood_group_choices,
        label='گروه خون',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # اطلاعات مدارک
    degree = forms.ChoiceField(
        choices=Soldier.degree_choices,
        label='مدرک تحصیلی',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    skill_certificate = forms.ChoiceField(
        choices=Soldier.skill_certificate_choices,
        label='نوع مدرک مهارتی',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    number_of_certificates = forms.IntegerField(
        label='تعداد مدرک',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    is_certificate = forms.BooleanField(
        label='مدرک مهارت آموزی دارد؟',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    skill_group = forms.ChoiceField(
        choices=Soldier.skill_group_choices,
        label='گروه مهارتی',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    has_driving_license = forms.ChoiceField(
        choices=Soldier.has_driving_license_choices,
        label='گواهی نامه',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class SoldierPhotoForm(forms.ModelForm):
    class Meta:
        model = Soldier
        fields = ['photo_scan']


class PhotoZipUploadForm(forms.Form):
    zip_file = forms.FileField(label='فایل ZIP شامل عکس‌ها')


class SoldierFormUpdate(forms.ModelForm):
    residence_province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        empty_label="انتخاب استان",
        widget=forms.Select(attrs={"class": "form-control", "id": "province-select"}),
        label='استان'
    )

    residence_city = forms.ModelChoiceField(
        queryset=City.objects.none(),  # ابتدا خالی می‌گذاریم تا با AJAX پر شود
        empty_label="انتخاب شهر",
        widget=forms.Select(attrs={"class": "form-control", "id": "city-select"}),
        label='شهر',
    )
    organizational_code = forms.ModelChoiceField(
        queryset=OrganizationalCode.objects.filter(is_active=False).all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='کدسازمانی',
    )

    rank = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.RANK_CHOICES,  # اگر در مدل Soldier مقدار choices تعریف شده
        label='درجه',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    current_parent_unit = forms.ModelChoiceField(
        queryset=ParentUnit.objects.all(),
        empty_label="انتخاب واحد اصلی",
        widget=forms.Select(attrs={"class": "form-control", "id": "parent-unit-select"}),
        label='قسمت', required=False,
    )

    current_sub_unit = forms.ModelChoiceField(
        queryset=SubUnit.objects.none(),  # مقدار اولیه خالی، بعداً با AJAX پر می‌شود
        empty_label="انتخاب زیرواحد",
        widget=forms.Select(attrs={"class": "form-control", "id": "sub-unit-select"}),
        label='زیرقسمت',
        required=False,
    )

    basic_training_center = forms.ModelChoiceField(
        queryset=TrainingCenter.objects.all(),  # فرض بر این است که مراکز آموزشی در این مدل ذخیره شده‌اند
        empty_label="انتخاب کنید...",
        label='نام آموزشگاه رزم مقدماتی',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    marital_status = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.MARITAL_STATUS_CHOICES,  # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='وضعیت تأهل',
        required=False,
    )

    health_status = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.HEALTH_STATUS_CHOICES,  # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='وضعیت سلامت',
        required=False
    )
    is_guard_duty = forms.ChoiceField(
        choices=Soldier.is_guard_duty_CHOICES,  # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='پاسدار وظیفه',
        required=False,

    )
    is_certificate = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.need_certificate_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='مدرک مهارت آموزی دارد؟',
        required=False,
    )
    skill_certificate = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.skill_certificate_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='نوع مدرک مهارتی',
        required=False,
    )
    independent_married = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.independent_married_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='متاهل مستقل',
        required=False,
    )
    skill_group = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.skill_group_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='گروه مهارتی',
        required=False,
    )
    blood_group = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.blood_group_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='گروه خون',
        required=False,
    )
    birth_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تاریخ تولد را وارد کنید'}),
        label='تاریخ تولد',
    )
    dispatch_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تاریخ اعزام را وارد کنید'}),
        label='تاریخ اعزام',
    )
    service_entry_date = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تاریخ ورود به یگان را وارد کنید'}),
        label='تاریخ ورود به یگان',
    )

    degree = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.degree_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='مدرک تحصیلی',
        required=False,
    )
    traffic_status = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.traffic_status_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='تردد',
        required=False,
    )
    is_sunni = forms.BooleanField(
        required=False,  # به صورت پیش‌فرض مقدار True یا False می‌گیرد
        label="اهل تسنن؟",  # اضافه کردن برچسب
        initial=False  # مقدار پیش‌فرض False است
    )
    is_needy = forms.BooleanField(
        required=False,  # به صورت پیش‌فرض مقدار True یا False می‌گیرد
        label="معسرین؟",  # اضافه کردن برچسب
        initial=False  # مقدار پیش‌فرض False است
    )
    Is_the_Basij_sufficient = forms.BooleanField(
        required=False,  # به صورت پیش‌فرض مقدار True یا False می‌گیرد
        label="کفایتدار بسیج؟",  # اضافه کردن برچسب
        initial=False  # مقدار پیش‌فرض False است
    )

    class Meta:
        model = Soldier
        fields = ['national_code', 'first_name', 'last_name', 'father_name', 'birth_place', 'issuance_place',
                  'address', 'postal_code', 'phone_mobile', 'phone_virtual', 'phone_parents', 'phone_home',
                  'id_card_code', 'card_chip', 'training_duration', 'essential_service_duration', 'number_of_children',
                  'health_status_description', 'is_needy', 'number_of_certificates', 'field_of_study', 'expertise',
                  'driving_license_type', 'referral_person', 'Is_the_Basij_sufficient', 'is_sunni', 'traffic_status',
                  'degree', 'service_entry_date', 'dispatch_date', 'birth_date', 'blood_group', 'skill_group',
                  'independent_married', 'skill_certificate', 'is_certificate', 'is_guard_duty', 'health_status',
                  'marital_status',
                  'basic_training_center', 'residence_city', 'residence_province', 'organizational_code',
                  'current_sub_unit', 'current_parent_unit','rank']
        widgets = {
            # ۱. اطلاعات هویتی و شناسایی
            'national_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کدملی را وارد کنید'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام را وارد کنید'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی را وارد کنید'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام پدر را وارد کنید'}),
            'birth_place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'محل تولد را وارد کنید'}),
            'issuance_place': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'محل صدور شناسنامه را وارد کنید'}),

            # ۲. اطلاعات تماس و محل سکونت
            'address': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'آدرس منزل را وارد کنید', 'rows': '3'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کدپستی را وارد کنید'}),
            'phone_mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'موبایل را وارد کنید'}),
            'phone_virtual': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'همراه مجازی را وارد کنید'}),
            'phone_parents': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'همراه پدر یا مادر را وارد کنید'}),
            'phone_home': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'منزل را وارد کنید'}),

            # ۳. اطلاعات سازمانی و خدمتی
            'id_card_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد پاسداری را وارد کنید'}),
            'card_chip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تراشه/کارت را وارد کنید'}),
            # ۴. وضعیت خدمتی و سوابق
            'training_duration': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'مدت آموزش (روز) را وارد کنید'}),
            'essential_service_duration': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'مدت خدمت ضرورت را وارد کنید'}),
            # ۵. وضعیت خانوادگی و اجتماعی
            'number_of_children': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'تعداد اولاد را وارد کنید'}),
            # ۶. وضعیت سلامت و مدارک پزشکی
            'health_status_description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'توضیحات وضعیت سلامت را وارد کنید'}),
            # ۷. مهارت‌ها و سوابق آموزشی
            'is_needy': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'معسرین را وارد کنید'}),
            'number_of_certificates': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'تعداد را وارد کنید'}),
            # ۹. اطلاعات بسیج و عقیدتی
            # ۱۰. اطلاعات مرتبط با مدارک و استعلامات
            'field_of_study': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'توضیحات رشته تحصیلی را وارد کنید'}),
            'expertise': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'توضیحات تخصص را وارد کنید'}),
            'driving_license_type': forms.CheckboxSelectMultiple(),
            'referral_person': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'معرف را وارد کنید'}),
        }

        def clean_national_code(self):
            national_code = self.cleaned_data.get('national_code')
            # اینجا می‌توانید شرط‌های خود را اعمال کنید
            find_soldire = Soldier.objects.filter(national_code=national_code).filter()
            if find_soldire is not None:
                raise forms.ValidationError("سرباز با این کدملی موجود دارد.")
            if national_code and len(national_code) != 10:
                raise forms.ValidationError("کد ملی باید دقیقاً ۱۰ رقم باشد.")
            return national_code

        def clean_is_guard_duty(self):
            is_guard_duty = self.cleaned_data.get('is_guard_duty')
            if is_guard_duty == "بلی":
                return True
            if is_guard_duty == "خیر":
                return False
