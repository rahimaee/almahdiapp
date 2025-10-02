from django import forms
from units_apps.models import ParentUnit
import jdatetime

MONTH_CHOICES = [(i, f"{i}") for i in range(1, 13)]

class ReportType2Form(forms.Form):
    unit = forms.ModelChoiceField(
        queryset=ParentUnit.objects.all(),
        label="نام قسمت",
        required=False,
        empty_label="انتخاب کنید"
    )
    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label="ماه",
        initial=jdatetime.date.today().month
    )
    base_date = forms.DateField(
        label="تاریخ مبنا",
        widget=forms.DateInput(attrs={'type': 'text', 'class': 'jalali-date'}),
        initial=jdatetime.date.today().strftime('%Y/%m/%d')
    )
