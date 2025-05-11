from django import forms
from .models import LeaveBalance


class LeaveBalanceForm(forms.ModelForm):
    class Meta:
        model = LeaveBalance
        exclude = ['annual_leave_remaining', 'incentive_leave_remaining', 'sick_leave_remaining','soldier']  # حذف فیلدها

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # افزودن استایل بوت استرپ
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
