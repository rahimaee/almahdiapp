from django.db import models

class Pasdar(models.Model):
    code = models.CharField("کد پاسداری", max_length=20, unique=True)
    first_name = models.CharField("نام", max_length=50)
    last_name = models.CharField("نام خانوادگی", max_length=50)
    national_id = models.CharField("شماره ملی", max_length=10, unique=True)
    birth_certificate_no = models.CharField("شماره شناسنامه", max_length=20, blank=True, null=True)
    section = models.CharField("قسمت حاضر", max_length=50, blank=True, null=True)
    role_in_section = models.CharField("نقش در قسمت", max_length=50, blank=True, null=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.full_name}"

    # نام کامل
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # خلاصه اطلاعات
    @property
    def short_info(self):
        info = f"{self.code} - {self.full_name}"
        if self.section:
            info += f" | {self.section}"
        if self.role_in_section:
            info += f" ({self.role_in_section})"
        return info

    # بررسی وجود بخش
    @property
    def has_section(self):
        return bool(self.section)

    # نقش یا مقدار پیش‌فرض
    @property
    def role_or_default(self):
        return self.role_in_section if self.role_in_section else "بدون نقش"
