from django.db import models

# Create your models here.

class LeaveBalance(models.Model):
    soldier = models.ForeignKey('soldires_apps.Soldier', on_delete=models.CASCADE)
    # سقف مرخصی‌ها
    annual_leave_quota = models.PositiveIntegerField("سقف مرخصی استحقاقی", default=0)
    incentive_leave_quota = models.PositiveIntegerField("سقف مرخصی تشویقی", default=0)
    sick_leave_quota = models.PositiveIntegerField("سقف مرخصی استعلاجی", default=0)

    # تعداد مرخصی استفاده شده
    annual_leave_used = models.PositiveIntegerField("تعداد مرخصی استحقاقی استفاده شده", default=0)
    incentive_leave_used = models.PositiveIntegerField("تعداد مرخصی تشویقی استفاده شده", default=0)
    sick_leave_used = models.PositiveIntegerField("تعداد مرخصی استعلاجی استفاده شده", default=0)

    # تعداد مرخصی باقی مانده
    annual_leave_remaining = models.PositiveIntegerField("تعداد مرخصی استحقاقی مانده", default=0)
    incentive_leave_remaining = models.PositiveIntegerField("تعداد مرخصی تشویقی مانده", default=0)
    sick_leave_remaining = models.PositiveIntegerField("تعداد مرخصی استعلاجی مانده", default=0)

    # سقف مازاد
    extra_sick_leave_quota = models.PositiveIntegerField("سقف مازاد استعلاجی", default=0)
    extra_annual_leave_quota = models.PositiveIntegerField("سقف مازاد استحقاقی", default=0)

    def __str__(self):
        return f"Leave Balance (ID: {self.id})"
