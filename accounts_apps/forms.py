# forms.py

from django import forms
from .models import ManagerPermission

class ManagerPermissionForm(forms.ModelForm):
    class Meta:
        model = ManagerPermission
        fields = ['manager', 'permission', 'granted_by']
