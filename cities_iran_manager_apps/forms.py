from django import forms
from .models import Province, City


class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ["name", "tel_prefix", "native"]


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ["name", "province", "distance"]
