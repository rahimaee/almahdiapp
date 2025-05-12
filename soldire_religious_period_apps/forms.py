from django import forms
from .models import ReligiousPeriod
from soldires_apps.models import Soldier


class ReligiousPeriodForm(forms.ModelForm):
    class Meta:
        model = ReligiousPeriod
        fields = ['name', 'date', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام دوره عقیدتی'}),
            'date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تاریخ دوره'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'توضیحات'}),
        }


class SoldierIdeologicalForm(forms.ModelForm):
    class Meta:
        model = Soldier
        fields = ['ideological_training_period']
        labels = {
            'ideological_training_period': 'دوره عقیدتی',
        }
        widgets = {
            'ideological_training_period': forms.Select(attrs={
                'class': 'form-control'
            })
        }


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label="آپلود فایل اکسل")
