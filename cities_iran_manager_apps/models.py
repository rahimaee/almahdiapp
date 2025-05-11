from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tel_prefix = models.CharField(max_length=10, blank=True, null=True)
    native = models.BooleanField(default=False, verbose_name='بومی')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cities")
    distance = models.FloatField(default=0, blank=True, null=True, verbose_name='مسافت')

    def __str__(self):
        return f"{self.name} ({self.province.name})"
