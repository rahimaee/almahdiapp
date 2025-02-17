from django import forms
from .models import Soldier, OrganizationalCode
from training_center_apps.models import TrainingCenter
from units_apps.models import ParentUnit, SubUnit
from cities_iran_manager_apps.models import City, Province
from django_jalali.forms import jDateField
from django_jalali.admin.widgets import AdminjDateWidget


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
        empty_label=OrganizationalCode.objects.filter(is_active=False).first(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='کدسازمانی',
    )

    rank = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.RANK_CHOICES,  # اگر در مدل Soldier مقدار choices تعریف شده
        label='درجه',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    current_parent_unit = forms.ModelChoiceField(
        queryset=ParentUnit.objects.all(),
        empty_label="انتخاب واحد اصلی",
        widget=forms.Select(attrs={"class": "form-control", "id": "parent-unit-select"}),
        label='قسمت'
    )

    current_sub_unit = forms.ModelChoiceField(
        queryset=SubUnit.objects.none(),  # مقدار اولیه خالی، بعداً با AJAX پر می‌شود
        empty_label="انتخاب زیرواحد",
        widget=forms.Select(attrs={"class": "form-control", "id": "sub-unit-select"}),
        label='زیرقسمت'
    )

    basic_training_center = forms.ModelChoiceField(
        queryset=TrainingCenter.objects.all(),  # فرض بر این است که مراکز آموزشی در این مدل ذخیره شده‌اند
        empty_label="انتخاب کنید...",
        label='نام آموزشگاه رزم مقدماتی',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    marital_status = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.MARITAL_STATUS_CHOICES,  # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='وضعیت تأهل',
    )

    health_status = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.HEALTH_STATUS_CHOICES,  # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='وضعیت سلامت'
    )
    is_guard_duty = forms.ChoiceField(
        choices=Soldier.is_guard_duty_CHOICES,  # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='پاسدار وظیفه',

    )
    is_certificate = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.need_certificate_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='مدرک مهارت آموزی دارد؟'
    )
    skill_certificate = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.skill_certificate_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='نوع مدرک مهارتی'
    )
    independent_married = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.independent_married_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='متاهل مستقل',
    )
    skill_group = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.skill_group_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='گروه مهارتی',
    )
    blood_group = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.blood_group_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='گروه خون',
    )
    birth_date = jDateField(
        widget=AdminjDateWidget(attrs={'class': 'form-control', 'placeholder': 'تاریخ تولد را وارد کنید'}),
        input_formats=["%Y-%m-%d", "%Y/%m/%d"],
    )
    dispatch_date = jDateField(
        widget=AdminjDateWidget(attrs={'class': 'form-control', 'placeholder': 'تاریخ اعزام را وارد کنید'}),
        input_formats=["%Y-%m-%d", "%Y/%m/%d"],
    )
    service_entry_date = jDateField(
        widget=AdminjDateWidget(attrs={'class': 'form-control', 'placeholder': 'تاریخ ورود به یگان را وارد کنید'}),
        input_formats=["%Y-%m-%d", "%Y/%m/%d"],
    )
    has_driving_license = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.has_driving_license_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='گواهی نامه',
    )
    degree = forms.ChoiceField(
        choices=[('', 'انتخاب کنید...')] + Soldier.degree_choices,
        # اگر در مدل Soldier مقدار choices تعریف شده
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='مدرک تحصیلی',
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
            # ۱۱. سایر اطلاعات مرتبط با خدمت

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
