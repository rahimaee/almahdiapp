from django import forms
from persiantools.jdatetime import JalaliDate

def shamsi_to_gregorian(value: str):
    """
    تبدیل تاریخ شمسی (YYYY/MM/DD) به میلادی (datetime.date)
    """
    if not value:
        return None
    value = value.strip()
    persian_numbers = '۰۱۲۳۴۵۶۷۸۹'
    english_numbers = '0123456789'
    for p, e in zip(persian_numbers, english_numbers):
        value = value.replace(p, e)
    try:
        year, month, day = map(int, value.split('/'))
        return JalaliDate(year, month, day).to_gregorian()
    except Exception:
        raise forms.ValidationError("تاریخ نامعتبر است")
