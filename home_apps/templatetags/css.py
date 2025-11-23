from django import template

register = template.Library()

def _safe_bound_field(field):
    """
    در صورتی که به جای BoundField، widget یا چیز دیگری فرستاده شد،
    تلاش می‌کنیم به نحو مطمئن به attrs دسترسی پیدا کنیم.
    """
    # BoundField (مثلاً {{ form.field }}) معمولا .field دارد
    if hasattr(field, 'field') and hasattr(field.field, 'widget'):
        return field, field.field.widget
    # اگر مستقیماً یک widget داده شد
    if hasattr(field, 'attrs'):
        return None, field
    # هیچ‌کدام: مقدار را بدون تغییر برمی‌گردانیم
    return None, None

def _update_attrs(field, **kwargs):
    """
    آپدیت امن attrs برای widget
    بازمی‌گرداند:
      - اگر BoundField بوده باشد، همان BoundField را بازمی‌گردانیم (برای رندر در تمپلیت)
      - در غیر این صورت، widget را بازمی‌گردانیم (نادری)
    """
    bound_field, widget = _safe_bound_field(field)
    if widget is None:
        return field  # چیزی برای بروزرسانی نبود؛ فقط همان را برمی‌گردانیم

    # به‌جای استفاده از کلمه‌ی کلیدی 'class' به‌صورت مستقیم از دیکشنری استفاده می‌کنیم
    widget.attrs.update(kwargs)
    return bound_field if bound_field is not None else widget


# -------------------------------
#   فیلترهای CSS
# -------------------------------

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    اضافه کردن یک کلاس (یا لیستی از کلاس‌ها که با فاصله جدا شده‌اند)
    مثال: {{ form.username|add_class:"ui-input" }}
    """
    existing = ''
    bound_field, widget = _safe_bound_field(field)
    if widget is not None:
        existing = widget.attrs.get('class', '')

    # ترکیب کلاس‌ها (از تکرار ساده جلوگیری نکرده ایم؛ اگر لازم است می‌توانیم مجموعه بسازیم)
    new_class = f"{existing} {css_class}".strip()
    return _update_attrs(field, **{'class': new_class})


@register.filter(name='add_classes')
def add_classes(field, classes):
    """
    اضافه کردن چند کلاس با فاصله (مکانیسم شبیه add_class)
    مثال: {{ form.username|add_classes:"ui-input another-class" }}
    """
    return add_class(field, classes)


@register.filter(name='set_class')
def set_class(field, css_class):
    """
    جایگزینی تمام کلاس‌ها با کلاس جدید
    مثال: {{ form.username|set_class:"form-control-lg" }}
    """
    return _update_attrs(field, **{'class': css_class})


@register.filter(name='remove_class')
def remove_class(field, css_class):
    """
    حذف یک کلاس مشخص از attribute class
    مثال: {{ form.username|remove_class:"old-class" }}
    """
    bound_field, widget = _safe_bound_field(field)
    if widget is None:
        return field

    existing = widget.attrs.get('class', '')
    classes = [c for c in existing.split() if c and c != css_class]
    return _update_attrs(field, **{'class': " ".join(classes)})


@register.filter(name='attr')
def set_attr(field, args):
    """
    ست کردن یک اتریبیوت دلخواه برای فیلد
    فرمت args: key:value
    """
    try:
        key, value = args.split(":", 1)
    except ValueError:
        return field

    # کپی از attrs فعلی و اضافه کردن جدید
    attrs = field.field.widget.attrs.copy()
    attrs[key] = value

    # ایجاد یک widget جدید با attrs جدید
    field.field.widget = field.field.widget.__class__(attrs=attrs)
    return field

@register.filter(name='style')
def add_style(field, style):
    """
    اضافه کردن استایل inline (ادغام با استایل قبلی اگر وجود داشته باشد)
    مثال: {{ field|style:"border:2px solid red;" }}
    """
    bound_field, widget = _safe_bound_field(field)
    if widget is None:
        return field

    existing = widget.attrs.get('style', '')
    if existing:
        # اطمینان از قرار گرفتن ; بین استایل‌ها
        if not existing.strip().endswith(';'):
            existing = existing.strip() + ';'
        new_style = f"{existing} {style}".strip()
    else:
        new_style = style

    return _update_attrs(field, style=new_style)
