from django.db import models


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
    service_end_date = models.DateField("تاریخ پایان خدمت اصلی", null=True, blank=True)
    actual_service_end_date = models.DateField("پایان خدمت اصلی", null=True, blank=True)
    calculate_until_date = models.DateField("محاسبه تا تاریخ", null=True, blank=True)

    # خدمت به روز
    main_service_days = models.PositiveIntegerField("خدمت اصلی به روز", default=0,blank=True,null=True)
    secondary_service_days = models.PositiveIntegerField("کمکی (خدمت اصلی)", default=0,blank=True,null=True)

    # خدمت دوره ضرورت
    mandatory_service_months = models.PositiveIntegerField("خدمت دوره ضرورت (به ماه)", default=0,blank=True,null=True)
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

    def save(self, *args, **kwargs):
        self.calculate_reduction_total()
        self.calculate_addition_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"خدمت سربازی {self.start_date} - {self.service_end_date}"
