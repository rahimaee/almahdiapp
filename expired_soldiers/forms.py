from django import forms
from .models import ExpiredSoldier
from .enums import EXPIRED_REASON_CHOICES

class ExpiredSoldierFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="نام / کد ملی",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "نام یا کد ملی"
        })
    )

    settlement_reason = forms.ChoiceField(
        required=False,
        choices=[("", "همه دلایل")] + EXPIRED_REASON_CHOICES,
        label="دلیل تسویه",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    end_service_start = forms.DateField(
        required=False,
        label="پایان خدمت از",
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        })
    )
    end_service_end = forms.DateField(
        required=False,
        label="پایان خدمت تا",
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        })
    )

    settlement_start = forms.DateField(
        required=False,
        label="تاریخ تسویه از",
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        })
    )
    settlement_end = forms.DateField(
        required=False,
        label="تاریخ تسویه تا",
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        })
    )
