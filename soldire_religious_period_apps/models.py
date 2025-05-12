from django.db import models


# Create your models here.


class ReligiousPeriod(models.Model):
    name = models.CharField(max_length=250, verbose_name='نام دوره عقیدتی', null=True, blank=True)
    date = models.CharField(max_length=250, verbose_name='دوره عقیدتی', null=True, blank=True)
    description = models.CharField(max_length=250, verbose_name='توضیحات', null=True, blank=True)

    def __str__(self):
        return f"{self.name}- {self.date}"
