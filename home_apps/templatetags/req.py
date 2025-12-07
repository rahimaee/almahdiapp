from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active_link(context, full_name, className='active-link'):
    """
    full_name باید به صورت:
        'namespace:url_name'
    یا فقط:
        'url_name'
    باشد
    """
    request = context.get('request')
    if not request or not hasattr(request, 'resolver_match'):
        return ''

    resolver = request.resolver_match

    # مقدار ورودی را تجزیه کنیم
    if ':' in full_name:
        ns, name = full_name.split(':', 1)
    else:
        ns, name = None, full_name

    # چک url_name
    match_name = resolver.url_name
    match_namespace = resolver.namespace  # تک فضای نام
    match_namespaces = resolver.namespaces  # لیست فضای‌نام‌ها

    # مقایسه url_name
    if name != match_name:
        return ''

    # اگر namespace مشخص شده، باید تطابق داشته باشد
    if ns and ns not in match_namespaces:
        return ''

    return className


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
