from django.db import models


# Create your models here.


class NaserinGroup(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name='نام گروه')
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name='توضیحات')
    manager = models.ForeignKey('accounts_apps.MyUser', on_delete=models.CASCADE, related_name="manager_nasserin",
                                verbose_name='مدیر گروه')

    def __str__(self):
        return f" گروه:{self.name} سرگروه: {self.manager.get_full_name()}"
