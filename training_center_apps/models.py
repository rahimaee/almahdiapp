from django.db import models

# Create your models here.
class TrainingCenter(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام مرکز آموزشی")
    is_active = models.BooleanField(default=True, verbose_name="فعال؟")

    def __str__(self):
        return self.name
