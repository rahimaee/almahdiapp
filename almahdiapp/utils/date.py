from django import forms
from persiantools.jdatetime import JalaliDate
import jdatetime

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

def gtosh(value=None):
    print(value)
    if value:
        try:
            j_dt = jdatetime.datetime.fromgregorian(datetime=value)
            return j_dt.strftime("%Y/%m/%d")
        except Exception:
            return value
    return ''