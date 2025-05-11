from django.db import models
from django.utils.timezone import now


class ParentUnit(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام واحد اصلی")

    class Meta:
        verbose_name = "واحد اصلی"
        verbose_name_plural = "واحدهای اصلی"

    def __str__(self):
        return self.name


class SubUnit(models.Model):
    WORK_TYPE_CHOICES = [('اداری', 'اداری'), ('شیفتی', 'شیفتی'), ('پستی', 'پستی')]
    name = models.CharField(max_length=255, verbose_name="نام زیرواحد")
    parent_unit = models.ForeignKey(
        ParentUnit, on_delete=models.CASCADE, related_name='sub_units', verbose_name="واحد اصلی"
    )
    work_type = models.CharField(
        choices=WORK_TYPE_CHOICES,
        verbose_name='تردد',
        null=True,
        blank=True,
        max_length=50,
    )

    class Meta:
        verbose_name = "زیرواحد"
        verbose_name_plural = "زیرواحدها"

    def __str__(self):
        return self.name


class UnitHistory(models.Model):
    soldier = models.ForeignKey(
        "soldires_apps.Soldier", on_delete=models.CASCADE, related_name="unit_history", verbose_name="سرباز"
    )
    parent_unit = models.ForeignKey(
        "ParentUnit", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="واحد اصلی"
    )
    sub_unit = models.ForeignKey(
        "SubUnit", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="زیرواحد"
    )
    start_date = models.DateTimeField(default=now, verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ پایان")
    skill_training_workshop = models.BooleanField(default=False, verbose_name='کارگاه مهات آموزی')

    class Meta:
        verbose_name = "تاریخچه بخش خدمت"
        verbose_name_plural = "تاریخچه بخش‌های خدمت"

    def __str__(self):
        return f"{self.soldier} - {self.parent_unit} - {self.sub_unit} ({self.start_date} تا {self.end_date})"
