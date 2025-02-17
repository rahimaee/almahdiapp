from django import forms
from .models import SoldierService


class SoldierServiceForm(forms.ModelForm):
    class Meta:
        model = SoldierService
        fields = '__all__'
        exclude = ['soldier']
