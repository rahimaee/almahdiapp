from django import forms
from .models import Province, City

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ["name", "slug", "tel_prefix", "native"]

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ["name", "slug", "province", "distance"]