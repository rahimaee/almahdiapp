from soldire_letter_apps.models import ClearanceLetter
from django import forms

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