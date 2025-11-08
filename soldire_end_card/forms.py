from django import forms

from soldires_apps.models import Soldier
from .models import CardSeries, CardSend


class CardSeriesForm(forms.ModelForm):
    class Meta:
        model = CardSeries
        fields = ['title', 'send_date', 'status', 'description']
        widgets = {
            'send_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':5}),
        }


class CardSendReviewForm(forms.ModelForm):
    class Meta:
        model = CardSend
        fields = ["is_checked", "is_issued", "review_date", "note"]
        widgets = {
            'review_date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }


class CardSeriesSelectForm(forms.Form):
    series = forms.ModelChoiceField(
        queryset=CardSeries.objects.all(),
        label="انتخاب سری جدید",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class CardSendForm(forms.ModelForm):
    class Meta:
        model = CardSend
        fields = ['series', 'soldier', 'is_checked', 'is_issued', 'review_date', 'note']
        widgets = {
            'series': forms.Select(attrs={'class': 'form-control select2'}),
            'soldier': forms.Select(attrs={'class': 'form-control select2'}),
            'review_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'note': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'series': 'سری کارت',
            'soldier': 'سرباز',
            'is_checked': 'بررسی شده',
            'is_issued': 'تحویل شده',
            'review_date': 'تاریخ بررسی',
            'note': 'توضیحات',
        }

    def __init__(self, *args, **kwargs):
        soldier_fixed = kwargs.pop('soldier_fixed', False)
        super().__init__(*args, **kwargs)

        if soldier_fixed:
            self.fields['soldier'].widget = forms.HiddenInput()
