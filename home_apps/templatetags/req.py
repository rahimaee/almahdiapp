from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active_link(context, url_name,className='active-link'):
    """
    بررسی می‌کند آیا مسیر فعلی برابر با url_name مشخص شده است یا نه.
    اگر بله، 'active-link' برمی‌گرداند، در غیر این صورت رشته خالی.
    """
    request = context.get('request')
    if request and hasattr(request, 'resolver_match'):
        if request.resolver_match.url_name == url_name:
            return className
    return ''

@register.filter
def lnumtrans(value=''):
    num = value
    if value:
        # جدا کردن قسمت عددی از باقی کلیدها
        parts = value.split('-')
        if parts:
            # آخرین بخش معمولاً عدد است
            num_part = parts[-1].lstrip('0')  # حذف صفرهای اول
            if not num_part:
                num_part = '0'  # اگر همه صفر بودند، حداقل 0 نمایش داده شود
            # جایگزینی بخش عددی با مقدار اصلاح شده
            parts[-1] = num_part
            num = '-'.join(parts)

    if value:
        num = num.replace('-','')
        num = num.replace('LTR','')
        num = num.replace('LT','')
        
        return num

    return value



@register.filter
def human_duration(days):
    """
    تبدیل تعداد روز به فرمت خوانا: سال، ماه، روز
    فرض می‌کنیم هر سال 365 روز و هر ماه 30 روز است.
    """
    try:
        days = int(days)
    except (ValueError, TypeError):
        return ''

    years, remainder = divmod(days, 365)
    months, days_left = divmod(remainder, 30)

    parts = []
    if years:
        parts.append(f"{years} سال" if years > 1 else "یک سال")
    if months:
        parts.append(f"{months} ماه" if months > 1 else "یک ماه")
    if days_left:
        parts.append(f"{days_left} روز" if days_left > 1 else "یک روز")

    return " و ".join(parts) if parts else "0 روز"
