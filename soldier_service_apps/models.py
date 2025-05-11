from django.db import models
import datetime
from dateutil.relativedelta import relativedelta
from django_jalali.db import models as jmodels
from soldires_apps.models import Soldier
from apps_settings.models import AppsSettings
from django.utils import timezone
from persiantools.jdatetime import JalaliDate
import jdatetime


class SoldierService(models.Model):
    soldier = models.ForeignKey('soldires_apps.Soldier', on_delete=models.CASCADE)
    reduction_veterans = models.PositiveIntegerField("کسری رزمندگان", default=0)
    reduction_disability = models.PositiveIntegerField("کسری جانبازی", default=0)
    reduction_bsj = models.PositiveIntegerField("کسری بسیج", default=0)
    reduction_project = models.PositiveIntegerField("کسری پروژه", default=0)
    reduction_children = models.PositiveIntegerField("کسری فرزند", default=0)
    reduction_spouse = models.PositiveIntegerField("کسری همسر", default=0)
    reduction_operational_areas = models.PositiveIntegerField("کسری مناطق عملیاتی", default=0)
    reduction_seniority = models.PositiveIntegerField("بخشش سنواتی", default=0)
    reduction_non_local = models.PositiveIntegerField("کسر غیربومی", default=0)
    reduction_system_adjustment = models.PositiveIntegerField("تطبیق با سامانه", default=0)
    reduction_other = models.PositiveIntegerField("غیره", default=0)
    reduction_total = models.PositiveIntegerField("مجموع کسری خدمت", default=0)

    # اضافه خدمت
    addition_seniority = models.PositiveIntegerField("سنواتی", default=0)
    addition_discipline = models.PositiveIntegerField("انضباطی", default=0)
    addition_gap = models.PositiveIntegerField("خلاء", default=0)
    addition_system = models.PositiveIntegerField("سامانه", default=0)
    addition_other = models.PositiveIntegerField("غیره", default=0)
    addition_total = models.PositiveIntegerField("مجموع اضافه خدمت", default=0)

    # تاریخ‌ها
    start_date = models.DateField("تاریخ اعزام", null=True, blank=True)
    service_end_date = models.DateField("تاریخ پایان خدمت اصلی(بدون کسر و اضافه خدمت)", null=True, blank=True)
    actual_service_end_date = models.DateField("پایان خدمت اصلی(یاکسر و اضافه خدمت)", null=True, blank=True)
    calculate_until_date = models.DateField("محاسبه تا تاریخ", null=True, blank=True)

    # خدمت به روز
    main_service_days = models.PositiveIntegerField("خدمت اصلی به روز", default=0, blank=True, null=True)
    secondary_service_days = models.PositiveIntegerField("کمکی (خدمت اصلی)", default=0, blank=True, null=True)

    # خدمت دوره ضرورت
    mandatory_service_months = models.PositiveIntegerField("خدمت دوره ضرورت (به ماه)", default=0, blank=True, null=True)
    notes = models.TextField("توضیحات", blank=True, null=True)

    def calculate_reduction_total(self):
        self.reduction_total = (
                self.reduction_veterans +
                self.reduction_disability +
                self.reduction_bsj +
                self.reduction_project +
                self.reduction_children +
                self.reduction_spouse +
                self.reduction_operational_areas +
                self.reduction_seniority +
                self.reduction_non_local +
                self.reduction_system_adjustment +
                self.reduction_other
        )

    def calculate_addition_total(self):
        self.addition_total = (
                self.addition_seniority +
                self.addition_discipline +
                self.addition_gap +
                self.addition_system +
                self.addition_other
        )

    def get_effective_service_months(self):
        # این تابع ماه‌های خدمت واقعی رو میده (۲۱ - کسری + اضافه خدمت)
        from apps_settings.models import AppsSettings
        app_settings = AppsSettings.objects.first()

        # مدت پایه خدمت
        base_months = int(app_settings.essential_service_duration) - int(app_settings.Length_of_service_in_the_unit)

        # محاسبه تعداد روز خدمت واقعی
        net_days = (base_months * 30) - self.reduction_total + self.addition_total

        # تبدیل به ماه
        return max(round(net_days / 30), 0)

    def get_effective_service_months(self):
        from apps_settings.models import AppsSettings
        app_settings = AppsSettings.objects.first()

        # مدت پایه خدمت برای مرخصی
        base_months = int(app_settings.Length_of_service_in_the_unit)
        base_days = base_months * 30

        # خدمت واقعی پس از کسری و اضافی
        net_days = base_days - self.reduction_total + self.addition_total

        # اگر کمتر از صفر بود، صفر بشه
        net_days = max(net_days, 0)

        # تبدیل به ماه
        return round(net_days / 30)

    def update_leave_balance_quota(self):
        from soldier_vacation_apps.models import LeaveBalance
        leave_balance, created = LeaveBalance.objects.get_or_create(soldier=self.soldier)

        net_months = self.get_effective_service_months()
        net_quota = round(net_months * 2.5)

        leave_balance.annual_leave_quota = net_quota
        leave_balance.annual_leave_remaining = max(net_quota - leave_balance.annual_leave_used, 0)
        leave_balance.save()

    def update_actual_service_end_date(self):
        if self.service_end_date is not None:
            # Convert Gregorian to Jalali
            jalali_date = jdatetime.date.fromgregorian(date=self.service_end_date)
            
            # Calculate total days to add/subtract
            total_days = self.addition_total - self.reduction_total
            
            # Add/subtract days in Jalali calendar
            jalali_date += datetime.timedelta(days=total_days)
            
            # Convert back to Gregorian
            self.actual_service_end_date = jalali_date.togregorian()
            
        else:
            from soldires_apps.models import Soldier
            from apps_settings.models import AppsSettings

            soldier = Soldier.objects.get(id=self.soldier.id)
            app_settings = AppsSettings.objects.first()
            start_date = soldier.dispatch_date

            if start_date:
                # Convert start date to Jalali
                start_date_jalali = jdatetime.date.fromgregorian(date=start_date)
                
                # Calculate total days to add/subtract
                total_days = self.addition_total - self.reduction_total
                
                # Calculate service_end_date (exactly 21 months = 630 days)
                service_end_datetime = datetime.datetime.combine(start_date_jalali.togregorian(), datetime.time())
                service_end_datetime = service_end_datetime + datetime.timedelta(days=630)  # 21 months * 30 days
                service_end_date = service_end_datetime.date()
                
                # Convert to Jalali for display
                service_end_jalali = jdatetime.date.fromgregorian(date=service_end_date)
                
                # Set service_end_date (without reductions/additions)
                self.service_end_date = service_end_date
                
                # Calculate actual_service_end_date with reductions/additions
                actual_end_datetime = service_end_datetime - datetime.timedelta(days=abs(total_days) if total_days < 0 else 0)
                actual_end_date = actual_end_datetime.date()
                
                # Convert back to Jalali for final date
                actual_end_jalali = jdatetime.date.fromgregorian(date=actual_end_date)
                
                # Set the actual service end date
                self.actual_service_end_date = actual_end_jalali.togregorian()

    def get_dispatch_date(self):
        from soldires_apps.models import Soldier
        soldier = Soldier.objects.get(id=self.soldier.id)
        self.start_date = soldier.dispatch_date

    def save(self, *args, **kwargs):
        self.calculate_reduction_total()
        self.calculate_addition_total()
        super().save(*args, **kwargs)  # اول ذخیره کن

        # سپس مرخصی را به‌روزرسانی کن
        self.update_leave_balance_quota()
        self.calculate_until_date = datetime.date.today()
        self.update_actual_service_end_date()
        self.get_dispatch_date()
        super().save(*args, **kwargs)  # اول ذخیره کن

    def __str__(self):
        return f"خدمت سربازی {self.start_date} - {self.service_end_date}"
