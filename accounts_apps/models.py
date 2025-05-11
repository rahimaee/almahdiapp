from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    # اضافه کردن فیلدهای اضافی
    national_code = models.CharField(max_length=10, unique=True, verbose_name="کد ملی")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="شماره تلفن")
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True,
                                        verbose_name="عکس پروفایل")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس")
    id_code = models.CharField(blank=True, null=True, max_length=50, verbose_name='کدپاسداری')
    units = models.ManyToManyField(
        'units_apps.ParentUnit',
        blank=True,
        verbose_name="واحدهای اصلی قابل مشاهده"
    )
    Employment_status = models.CharField(
        blank=True,
        null=True,
        max_length=150,
        choices=[('سرباز', 'سرباز'), ('پاسدار', 'پاسدار'), ('کارمند', 'کارمند')],
        verbose_name='وضعیت شاغل',
    )
    features = models.ManyToManyField(
        'Feature',
        blank=True,
        verbose_name="امکانات قابل دسترسی"
    )

    # متدهای اختیاری
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    def has_feature(self, feature_name):
        return self.features.filter(name=feature_name).exists()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_employment_status(self):
        return self.Employment_status


class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Section(models.Model):
    section_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.section_name


class Permission(models.Model):
    permission_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.permission_name


class ManagerPermission(models.Model):
    manager = models.ForeignKey('accounts_apps.MyUser', on_delete=models.CASCADE, related_name="manager_permissions")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    granted_by = models.ForeignKey('accounts_apps.MyUser', related_name="granted_permissions",
                                   on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.manager.username} - {self.permission.permission_name}'


class AccessHistory(models.Model):
    manager = models.ForeignKey('accounts_apps.MyUser', on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    change_date = models.DateTimeField(auto_now_add=True)
    change_description = models.TextField()

    def __str__(self):
        return f'{self.manager.username} - {self.permission.permission_name} - {self.change_date}'
