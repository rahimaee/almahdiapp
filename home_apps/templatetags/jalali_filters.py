import jdatetime
from django import template
import datetime

register = template.Library()
@register.filter
def to_jalali_to(date):
    return jdatetime.date.fromgregorian(date=date).strftime("%Y/%m/%d")

@register.filter
def to_jalali(value):
    if value:
        try:
            j_date = jdatetime.date.fromgregorian(date=value)
            return j_date.strftime('%Y/%m/%d')
        except:
            return value
    return ''

@register.filter
def to_jalali_g(value):
    if value:
        try:
            j_date = jdatetime.date.fromgregorian(date=value)
            return j_date.strftime('%Y-%m-%d')
        except:
            return value
    return ''

@register.filter
def to_end(value):
    if isinstance(value, (datetime.date, datetime.datetime)):
        try:
            # تبدیل تاریخ میلادی به شمسی
            shamsi_date = jdatetime.date.fromgregorian(date=value)
            today_shamsi = jdatetime.date.today()
            delta = today_shamsi - shamsi_date
            return delta.days
        except Exception as e:
            return f"خطا: {e}"
    return "تاریخ نامعتبر"
