from django import forms
from .models import SoldierService


from django_jalali.forms import jDateField, widgets as jwidgets

class SoldierServiceForm(forms.ModelForm):
    start_date = jDateField(
        label="تاریخ اعزام",
        widget=jwidgets.jDateInput(attrs={'class': 'form-control'}),
        required=False
    )
    service_end_date = jDateField(
        label="تاریخ پایان خدمت اصلی",
        widget=jwidgets.jDateInput(attrs={'class': 'form-control'}),
        required=False
    )
    actual_service_end_date = jDateField(
        label="پایان خدمت اصلی",
        widget=jwidgets.jDateInput(attrs={'class': 'form-control'}),
        required=False
    )
    calculate_until_date = jDateField(
        label="محاسبه تا تاریخ",
        widget=jwidgets.jDateInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = SoldierService
        fields = '__all__'
        exclude = ['soldier']