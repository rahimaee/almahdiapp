from django.db import models


class SoldierService(models.Model):
    soldier = models.ForeignKey('soldires_apps.Soldier', on_delete=models.CASCADE)
    # کسری خدمت
    ksr_razmangan = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ksr_janbazi = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ksr_basij = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ksr_project = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ksr_farzand = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ksr_hamsar = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ksr_mantaqe_amaliati = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # اضافه خدمت
    khod_dore_senavati = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    khod_enzebati = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    khod_khalla = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    khod_samane = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    khod_ghayre = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # محاسبه مجموع کسری و اضافه خدمت
    total_ksr = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_khod = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total_ksr = sum([self.ksr_razmangan, self.ksr_janbazi, self.ksr_basij,
                              self.ksr_project, self.ksr_farzand, self.ksr_hamsar,
                              self.ksr_mantaqe_amaliati])
        self.total_khod = sum([self.khod_dore_senavati, self.khod_enzebati,
                               self.khod_khalla, self.khod_samane, self.khod_ghayre])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"کسری و اضافه خدمت برای سرباز {self.soldier}"
