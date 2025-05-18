from django.db import models


# Create your models here.
class EscapeRecord(models.Model):
    soldier = models.ForeignKey('soldires_apps.Soldier', on_delete=models.CASCADE, related_name='escapes')
    start_date = models.DateField(verbose_name="تاریخ شروع فرار")
    return_date = models.DateField(null=True, blank=True, verbose_name="تاریخ بازگشت از فرار")
    note = models.TextField(blank=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "سابقه فرار"
        verbose_name_plural = "سوابق فرار"
        ordering = ['-start_date']

    def __str__(self):
        return f"فرار از {self.start_date} تا {self.return_date or 'نامشخص'} برای {self.soldier}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # به‌روزرسانی وضعیت سرباز
        soldier = self.soldier

        if self.return_date:
            # اگه این فرار به پایان رسیده باشه
            active_escapes = soldier.escapes.filter(return_date__isnull=True).exists()
            soldier.is_fugitive = active_escapes  # فقط اگه هنوز فراری هست
        else:
            # اگه فرار جدیدی بدون تاریخ بازگشت ثبت شده
            soldier.is_fugitive = True

        # بروزرسانی سابقه فرار
        total_escapes = soldier.escapes.count()
        soldier.fugitive_record = total_escapes

        soldier.save()
