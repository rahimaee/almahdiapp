# forms.py

from django import forms
from .models import ManagerPermission, Feature, MyUser
from units_apps.models import ParentUnit
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'id': 'username',
                   'placeholder': 'نام کاربری وارد کنید'}),
        label='ایمیل',

    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'type': 'password', 'id': 'password', 'class': 'form-control', 'name': 'password',
                   'placeholder': 'رمز عبور را وارد کنید', 'required': "ایمیل خود را وارد کنید"}),
        label='رمز عبور'
    )


class ManagerPermissionForm(forms.ModelForm):
    class Meta:
        model = ManagerPermission
        fields = ['manager', 'permission', 'granted_by']


class UserAccessForm(forms.ModelForm):
    units = forms.ModelMultipleChoiceField(
        queryset=ParentUnit.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = MyUser
        fields = ['units', 'features', ]


class MyUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'national_code', 'phone_number', 'profile_picture',
            'address', 'id_code', 'Employment_status'
        ]
        widgets = {
            'Employment_status': forms.Select(attrs={'class': 'form-control'}),
        }


class MyUserProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = [
            'first_name', 'last_name', 'national_code', 'phone_number',
            'profile_picture', 'address', 'id_code', 'Employment_status',
            'units', 'features'
        ]
        widgets = {
            'Employment_status': forms.Select(attrs={'class': 'form-control'}),
            'units': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'features': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }
