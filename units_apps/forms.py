from django import forms
from .models import ParentUnit, SubUnit


class ParentUnitForm(forms.ModelForm):
    class Meta:
        model = ParentUnit
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام واحد اصلی'}),
        }


class SubUnitForm(forms.ModelForm):
    class Meta:
        model = SubUnit
        fields = ['name', 'parent_unit','work_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام زیرواحد'}),
            'parent_unit': forms.Select(attrs={'class': 'form-control'}),
            'work_type': forms.Select(attrs={'class': 'form-control'}),
        }
