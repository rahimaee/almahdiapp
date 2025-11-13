# organizational_position/templatetags/organizational_tags.py
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
    if value:
        num = value.replace('-','')
        num = num.replace('LTR','')
        num = num.replace('LT','')
        
        return num

    return value