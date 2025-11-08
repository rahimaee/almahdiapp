from django import forms
from units_apps.models import ParentUnit
import jdatetime

MONTH_CHOICES = [(i, f"{i} ماه بعد") for i in range(1, 13)]

class ReportType2Form(forms.Form):
    unit = forms.ModelChoiceField(
        queryset=ParentUnit.objects.all(),
        label="نام قسمت",
        required=False,
        empty_label="انتخاب کنید"
    )
    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label="ماه بعدی",
        initial=jdatetime.date.today().month
    )
    base_date = forms.DateField(
        label="تاریخ مبنا",
        widget=forms.DateInput(attrs={'type': 'text', 'class': 'jalali-date'}),
        initial=jdatetime.date.today().strftime('%Y/%m/%d')
    )

from django import forms
from units_apps.models import ParentUnit
import jdatetime
from dateutil.relativedelta import relativedelta

MONTH_CHOICES = [(i, f"{i} ماه بعد") for i in range(1, 13)]

class ReportType2Form(forms.Form):
    unit = forms.ModelChoiceField(
        queryset=ParentUnit.objects.all(),
        label="نام قسمت",
        required=False,
        empty_label="انتخاب کنید"
    )
    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label="ماه بعدی",
        required=True,
        initial=jdatetime.date.today().month
    )
    base_date = forms.CharField(
        label="تاریخ مبنا",
        widget=forms.DateInput(attrs={'type': 'text', 'class': 'jalali-date'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ مقدار پیش‌فرض برای نمایش در فرم
        self.default_unit = ParentUnit.objects.first()
        self.default_month = 1
        self.default_base_date = jdatetime.date.today()
        self.fields['unit'].initial = self.default_unit
        self.fields['month'].initial = self.default_month
        self.fields['base_date'].initial = self.default_base_date.strftime('%Y/%m/%d')

    def clean(self):
        cleaned_data = super().clean()
        month = cleaned_data.get('month')

        try:
            month = int(month)
        except (TypeError, ValueError):
            month = self.default_month
        unit = cleaned_data.get('unit') or self.default_unit
        base_date_str = cleaned_data.get('base_date')

        # ✅ تبدیل جلالی از رشته – اگر خراب بود fallback
        try:
            base_date_j = jdatetime.datetime.strptime(base_date_str, '%Y/%m/%d').date()
        except:
            base_date_j = self.default_base_date

        
        # ✅ محاسبه تاریخ‌ها
        base_date_g = base_date_j.togregorian()
        next_date_j = base_date_j + jdatetime.timedelta(days=month * 30)
        next_date_g = next_date_j.togregorian()
        # ✅ ذخیره در cleaned_data
        cleaned_data.update({
            'unit': unit,
            'month': month,
            'base_date': base_date_str,
            'base_date_j': base_date_j,
            'base_date_g': base_date_g,
            'next_date_j': next_date_j,
            'next_date_g': next_date_g
        })

        return cleaned_data