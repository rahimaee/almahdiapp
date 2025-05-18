from soldire_letter_apps.models import *
from django import forms

from soldires_apps.models import Soldier
from units_apps.models import SubUnit


# Create your views here.
class ClearanceLetterForm(forms.ModelForm):
    class Meta:
        model = ClearanceLetter
        fields = ['soldier', 'reason', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(ClearanceLetterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class NormalLetterJudicialInquiryForm(forms.ModelForm):
    soldier = forms.ModelChoiceField(
        queryset=Soldier.objects.all(),
        label='سرباز',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'توضیحات را وارد کنید'}),
        label='توضیحات',
        required=False,
    )

    class Meta:
        model = NormalLetterJudicialInquiry
        fields = ['soldier', 'reason', 'description']
        labels = {
            'reason': 'علت استعلام',
            'subject': 'موضوع',
            'description': 'توضیحات',
        }
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }


class NormalLetterDomesticSettlement(forms.ModelForm):
    soldier = forms.ModelChoiceField(
        queryset=Soldier.objects.all(),
        label='سرباز',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'توضیحات را وارد کنید'}),
        label='توضیحات',
        required=False,
    )

    class Meta:
        model = NormalLetterJudicialInquiry
        fields = ['soldier', 'reason', 'description']
        labels = {
            'reason': 'علت تسویه حساب',
            'subject': 'موضوع',
            'description': 'توضیحات',
        }
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }


class NormalLetterDomesticSettlementForm(forms.ModelForm):
    soldier = forms.ModelChoiceField(
        queryset=Soldier.objects.all(),
        label='سرباز',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'توضیحات را وارد کنید'}),
        label='توضیحات',
        required=False,
    )

    class Meta:
        model = NormalLetterJudicialInquiry
        fields = ['soldier', 'reason', 'description']
        labels = {
            'reason': 'علت تسویه حساب',
            'subject': 'موضوع',
            'description': 'توضیحات',
        }
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }


class IntroductionLetterForm(forms.ModelForm):
    class Meta:
        model = IntroductionLetter
        exclude = ['letter_number', 'status', 'created_at', 'updated_at', 'letter_type']
        widgets = {
            'soldier': forms.Select(attrs={'class': 'form-control'}),
            'part': forms.Select(attrs={'class': 'form-control'}),
            'sub_part': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_part'].queryset = SubUnit.objects.none()

        if 'part' in self.data:
            try:
                part_id = int(self.data.get('part'))
                self.fields['sub_part'].queryset = SubUnit.objects.filter(parent_unit_id=part_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.part:
            self.fields['sub_part'].queryset = self.instance.part.sub_units.all()


class MembershipCertificateForm(forms.ModelForm):
    destination_choice = forms.ChoiceField(
        label="مقصد نامه",
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    destination_manual = forms.CharField(
        label="مقصد دلخواه",
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'اگر مقصدی در لیست نبود، اینجا وارد کنید'})
    )

    class Meta:
        model = MembershipCertificate
        exclude = ['normal_letter']
        widgets = {
            'description_in': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'soldier': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        destinations = NormalLetter.objects.values_list('destination', flat=True).distinct()
        choices = [('', '--- انتخاب کنید ---')]
        choices += [(d, d) for d in destinations if d]
        choices.append(('custom', 'سایر (مقصد دلخواه)'))
        self.fields['destination_choice'].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        dest_choice = cleaned_data.get('destination_choice')
        dest_manual = cleaned_data.get('destination_manual')

        if dest_choice == 'custom':
            if not dest_manual:
                self.add_error('destination_manual', 'لطفاً مقصد دلخواه را وارد کنید.')
            cleaned_data['final_destination'] = dest_manual
        else:
            cleaned_data['final_destination'] = dest_choice

        return cleaned_data


class HealthIodineForm(forms.ModelForm):
    soldier = forms.ModelChoiceField(
        queryset=Soldier.objects.all(),
        label='سرباز',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = NormalLetterHealthIodine
        exclude = ['normal_letter']
        widgets = {
            'soldier': forms.Select(attrs={'class': 'form-control'}),
            'part': forms.Select(attrs={'class': 'form-control'}),
            'sub_part': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_part'].queryset = SubUnit.objects.none()

        if 'part' in self.data:
            try:
                part_id = int(self.data.get('part'))
                self.fields['sub_part'].queryset = SubUnit.objects.filter(parent_unit_id=part_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.part:
            self.fields['sub_part'].queryset = self.instance.part.sub_units.all()
