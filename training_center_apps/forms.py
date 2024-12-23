from django import forms
from .models import TrainingCenter


class TrainingCenterForm(forms.ModelForm):
    class Meta:
        model = TrainingCenter
        fields = ['name', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام مرکز آموزشی'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'نام مرکز آموزشی',
            'is_active': 'فعال',
        }
