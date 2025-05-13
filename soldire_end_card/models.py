from django.db import models


# Create your models here.
class CardSeries(models.Model):
    title = models.CharField("نام سری کارت", max_length=100)
    send_date = models.DateField("تاریخ ارسال سری")
    status = models.CharField(
        "وضعیت سری",
        max_length=20,
        choices=[
            ("preparing", "در حال آماده‌سازی"),
            ("sent", "ارسال شده"),
            ("checking", "در حال بررسی"),
            ("completed", "تکمیل شده"),
        ],
        default="preparing"
    )
    description = models.TextField("توضیحات", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def update_status(self):
        total = self.card_sends.count()
        checked = self.card_sends.filter(is_checked=True).count()

        if total > 0 and total == checked:
            self.status = "completed"
            self.save()

    def __str__(self):
        return f"{self.title} - {self.send_date}"


class CardSend(models.Model):
    series = models.ForeignKey(CardSeries, on_delete=models.CASCADE, related_name="card_sends")
    soldier = models.ForeignKey("soldires_apps.Soldier", on_delete=models.CASCADE, related_name="card_sends")

    is_checked = models.BooleanField("بررسی شد؟", default=False)
    is_issued = models.BooleanField("کارت صادر شده؟", default=False)

    review_date = models.DateField("تاریخ بررسی", blank=True, null=True)
    note = models.TextField("توضیحات", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.series.update_status()

    def __str__(self):
        return f"{self.soldier} - سری {self.series.title}"
