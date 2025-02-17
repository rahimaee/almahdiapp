from django import forms
from .models import SoldierDocuments


class SoldierDocumentsForm(forms.ModelForm):
    class Meta:
        model = SoldierDocuments
        fields ='__all__'
        exclude  = ['soldier']
