from django import forms
from .models import LeaveBalance


class LeaveBalanceForm(forms.ModelForm):
    class Meta:
        model = LeaveBalance
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # اضافه کردن کلاس‌های بوت استرپ به همه فیلدها
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # غیرفعال کردن فیلدهای باقیمانده (در صورت نیاز)
        readonly_fields = [
            'annual_leave_remaining',
            'incentive_leave_remaining',
            'sick_leave_remaining'
        ]

        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True
