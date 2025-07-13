from django import forms
from .models import NaserinGroup

class NaserinGroupForm(forms.ModelForm):
    class Meta:
        model = NaserinGroup
        fields = ['name', 'description', 'manager']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows':4}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
        }