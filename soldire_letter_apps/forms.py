from soldire_letter_apps.models import *
from django import forms

from soldires_apps.models import Soldier
from units_apps.models import SubUnit
import json
from .models import EssentialFormCardLetter


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

        first_choice_value = ClearanceLetter.CLEARANCE_REASON_CHOICES[0][0]
        self.fields['reason'].initial = first_choice_value
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


class CommitmentLetterForm(forms.ModelForm):
    soldier = forms.ModelChoiceField(
        queryset=Soldier.objects.all(),
        label='سرباز',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = NormalLetterCommitmentLetter
        exclude = ['normal_letter']
        widgets = {
            'soldier': forms.Select(attrs={'class': 'form-control'}),
            'type_card_chip': forms.Select(attrs={'class': 'form-control'}),
        }
        
import random
from .constants import *

class EssentialFormCardLetterForm(forms.ModelForm):
    # فقط این فیلد hidden است
    letter_id = forms.CharField(widget=forms.HiddenInput(),required=False)
    letter_type = forms.CharField(widget=forms.HiddenInput(), required=True)  # required=True

    # فیلدهای پیش‌فرض فرم (نه مدل)
    title = forms.CharField(
        label="موضوع",
        initial="تایید انجام دوره ضرورت سرباز منقضی خدمت",
        help_text="نام سرباز در انتهای موضوع قرار میگیرد.",
    )
    receiver = forms.CharField(
        label="گیرنده",
        initial="معاونت نیروی انسانی نزسا – مدیریت منابع انسانی سرباز – دایره صدور کارت",
        help_text="به",
    )
    sender = forms.CharField(
        label="فرستنده",
        initial="آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه - نیروی انسانی - منابع انسانی سرباز",
        help_text="از",
    )
 

    number = forms.CharField(
        label="شماره نامه",
        required=False,
        disabled=True,
        help_text="شماره نامه اتوماتیک"
    )
    class Meta:
        model = EssentialFormCardLetter
        fields = ['number', 'return_number', 'title',  'receiver','sender',  'description']
        labels = {
            "return_number": "شماره عطف",
            "description": "توضیحات",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


    def __init__(self, *args, **kwargs):
        form_type = kwargs.pop('form_type', None)
        super().__init__(*args, **kwargs)

        # تولید شماره نامه 10 رقمی فقط برای فرم جدید
        if not self.instance.pk:
            self.fields['number'].initial = str(random.randint(10**9, 10**10-1))

        # اگر instance موجود باشد یا initial، نوع فرم از آن گرفته شود
        if not form_type:
            if self.instance and self.instance.letter_type:
                form_type = self.instance.letter_type
            elif 'initial' in kwargs:
                form_type = kwargs['initial'].get('letter_type')

        self.fields['letter_type'].initial = form_type

        # بارگذاری مقادیر داینامیک
        form_data_dict = {}
        if self.instance:
            self.fields['letter_id'].initial = self.instance.id
            if self.instance.form_data:
                try:
                    form_data_dict = json.loads(self.instance.form_data)
                except json.JSONDecodeError:
                    pass

        if form_type:
            cls = FORM_CLASSES.get(form_type)
            for field_name, field_type in cls.__annotations__.items():
                if field_name in self.fields:
                    continue
                label = FIELD_LABELS.get(field_name, field_name.replace("_", " "))
                default_value = form_data_dict.get(field_name, getattr(cls(), field_name))
                
                if field_name in FIELD_CHOICES:
                    self.fields[field_name] = forms.ChoiceField(
                        label=label,
                        required=False,
                        choices=FIELD_CHOICES[field_name],
                        initial=default_value,
                    )
                elif field_name in ['main_image', 'normal_image']:
                    self.fields[field_name] = forms.ImageField(
                        label=label,
                        required=False,
                        initial=default_value if default_value else None
                    )
                elif field_type == int:
                    self.fields[field_name] = forms.IntegerField(
                        label=label,
                        required=False,
                        initial=default_value,
                        widget=forms.NumberInput(attrs={"dir": "ltr"})
                    )
                elif field_type == float:
                    self.fields[field_name] = forms.FloatField(
                        label=label,
                        required=False,
                        initial=default_value,
                        widget=forms.NumberInput(attrs={"dir": "ltr"})
                    )
                else:
                    self.fields[field_name] = forms.CharField(
                        label=label,
                        required=False,
                        initial=default_value
                    )

                self.fields[field_name].help_text = FIELD_LABELS_HELPER.get(field_name, "")
    
    def clean(self):
        cleaned_data = super().clean()
        form_type = cleaned_data.get('letter_type')
        cls = FORM_CLASSES.get(form_type)

        if cls:
            dynamic_data = {}
            for field_name in cls.__annotations__.keys():
                dynamic_data[field_name] = cleaned_data.pop(field_name, None)
            cleaned_data['form_data'] = json.dumps(dynamic_data, ensure_ascii=False)

        return cleaned_data
    def save(self, commit=True):
        instance = super().save(commit=False)
        print(instance)
        # ست کردن letter_type
        instance.letter_type = self.cleaned_data.get('letter_type') or instance.letter_type
        # ست کردن فرم داینامیک
        instance.form_data = self.cleaned_data.get('form_data')
        # ست کردن تصاویر
        for img_field in ['main_image', 'normal_image']:
            file = self.cleaned_data.get(img_field)
            if file:
                setattr(instance, img_field, file)

        if commit:
            instance.save()
        return instance