from django.db import models
from django.utils import timezone
class ClearanceLetter(models.Model):
    CLEARANCE_REASON_CHOICES = [
        ('service_completed', 'پایان خدمت'),
        ('university_admission', 'قبولی در دانشگاه'),
        ('transfer', 'انتقال'),
        ('permanent_exemption', 'معافیت دائم'),
    ]

    soldier = models.ForeignKey('soldires_apps.Soldier', on_delete=models.CASCADE, verbose_name="سرباز")
    reason = models.CharField(max_length=30, choices=CLEARANCE_REASON_CHOICES, verbose_name="علت تسویه حساب")
    letter_number = models.CharField(max_length=100, unique=True, verbose_name="شماره نامه", editable=False)
    issue_date = models.DateField(auto_now_add=True, verbose_name="تاریخ صدور تسویه کل")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "نامه تسویه‌حساب"
        verbose_name_plural = "نامه‌های تسویه‌حساب"

    def __str__(self):
        return f"{self.soldier} - {self.get_reason_display()} - {self.letter_number}"

    def save(self, *args, **kwargs):
        if not self.letter_number:
            # فرض بر این است که Soldier دارای فیلد national_code می‌باشد
            national_code = self.soldier.national_code[-4:]  # ۴ رقم آخر کد ملی
            date_part = timezone.now().strftime('%Y%m%d')  # تاریخ به صورت YYYYMMDD
            self.letter_number = f"CL-{national_code}-{date_part}"
            # اطمینان از یونیک بودن:
            counter = 1
            base_letter_number = self.letter_number
            while ClearanceLetter.objects.filter(letter_number=self.letter_number).exists():
                self.letter_number = f"{base_letter_number}-{counter}"
                counter += 1
        super().save(*args, **kwargs)