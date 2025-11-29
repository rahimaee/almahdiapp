from django.db import models
import datetime
from soldier_vacation_apps.models import LeaveBalance
from apps_settings.models import AppsSettings


class SoldierService(models.Model):
    soldier = models.OneToOneField('soldires_apps.Soldier', on_delete=models.CASCADE)
    # کسری خدمت
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

    # service_end_24m
    # service_end_21m
    def calculate_reduction_total(self):
        self.reduction_total = sum([
            self.reduction_veterans,
            self.reduction_disability,
            self.reduction_bsj,
            self.reduction_project,
            self.reduction_children,
            self.reduction_spouse,
            self.reduction_operational_areas,
            self.reduction_seniority,
            self.reduction_non_local,
            self.reduction_system_adjustment,
            self.reduction_other,
        ])

    def calculate_addition_total(self):
        self.addition_total = sum([
            self.addition_seniority,
            self.addition_discipline,
            self.addition_gap,
            self.addition_system,
            self.addition_other,
        ])

    def get_effective_service_months(self):
        settings = AppsSettings.objects.first()
        base_months_str = settings.Length_of_service_in_the_unit

        try:
            base_months = int(base_months_str)
        except (ValueError, TypeError):
            base_months = 21  # یا هر مقدار پیش‌فرض منطقی که مدنظرته

        base_days = base_months * 30
        net_days = max(base_days - self.reduction_total + self.addition_total, 0)
        return round(net_days / 30)

    def update_leave_balance_quota(self):
        leave_balance, _ = LeaveBalance.objects.get_or_create(soldier=self.soldier)
        net_months = self.get_effective_service_months()
        net_quota = round(net_months * 2.5)
        leave_balance.annual_leave_quota = net_quota
        leave_balance.annual_leave_remaining = max(net_quota - leave_balance.annual_leave_used, 0)
        leave_balance.save()

    def update_soldire_service_end_date(self):
        self.soldier.service_end_date = self.actual_service_end_date
        self.soldier.total_service_adjustment = self.addition_total - self.reduction_total
        self.soldier.save()

    def get_reduction_types_with_values(self):
        types = []

        def append_type(title, value):
            if value > 0:
                types.append(f"{title}: {value} روز")

        append_type("رزمندگان", self.reduction_veterans)
        append_type("جانباز", self.reduction_disability)
        append_type("بسیج", self.reduction_bsj)
        append_type("پروژه‌ای", self.reduction_project)
        append_type("فرزند", self.reduction_children)
        append_type("همسر", self.reduction_spouse)
        append_type("مناطق عملیاتی", self.reduction_operational_areas)
        append_type("بخشش سنواتی", self.reduction_seniority)
        append_type("غیربومی", self.reduction_non_local)
        append_type("تطبیق سامانه", self.reduction_system_adjustment)
        append_type("سایر", self.reduction_other)
        append_type("سنواتی", self.addition_seniority)
        append_type("انضباطی", self.addition_discipline)
        append_type("خلاء", self.addition_gap)
        append_type("سامانه", self.addition_system)
        append_type("سایر", self.addition_other)

        self.soldier.service_deduction_type = "، ".join(types) if types else "ندارد"
        self.soldier.save()

    def update_actual_service_end_date(self):
        if self.service_end_date:
            base_date = self.service_end_date
        else:
            if not self.soldier.dispatch_date:
                return
            base_date = self.soldier.dispatch_date + datetime.timedelta(days=630)
            self.service_end_date = base_date

        total_days = self.addition_total - self.reduction_total
        actual_end_date = base_date + datetime.timedelta(days=total_days)
        self.actual_service_end_date = actual_end_date

    def get_dispatch_date(self):
        self.start_date = self.soldier.dispatch_date

    def save(self, *args, **kwargs):
        self.calculate_reduction_total()
        self.calculate_addition_total()
        self.calculate_until_date = datetime.date.today()
        self.get_dispatch_date()
        self.update_actual_service_end_date()
        super().save(*args, **kwargs)
        self.update_leave_balance_quota()
        self.update_soldire_service_end_date()
        self.get_reduction_types_with_values()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"خدمت سربازی {self.start_date} - {self.service_end_date}"




def get_service(soldier):
        """
        دریافت یا ایجاد رکورد SoldierService به صورت ایمن.
        اگر رکورد از قبل وجود داشته باشد آن را برمی‌گرداند،
        در غیر این صورت رکورد جدید می‌سازد.
        """
        services = SoldierService.objects.filter(soldier=soldier).select_related('soldier')
        ser_c = services.count()
        service = None
        if ser_c > 1:
            services[1:].delete()
            
        
        if ser_c > 0:
            print(soldier)
            services[0].soldier = soldier
            services[0].save()
            return services[0]
        
        try:
            service = SoldierService()
            service.soldier = soldier
            service.save()

            # کسری بر اساس وضعیت تأهل
            if soldier.marital_status == 'متاهل':
                service.reduction_spouse = 60
                children = soldier.number_of_children
                if children >= 1:
                    service.reduction_children = 90
                if children >= 2:
                    service.reduction_children += 120
                if children >= 3:
                    service.reduction_children += 150
                service.save()
        except Exception as e:
            print(f"Error creating SoldierService: {str(e)}")
            raise
        return service
 