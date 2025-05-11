from django.db import models


# Create your models here.


class AppsSettings(models.Model):
    shoare_sall = models.CharField(max_length=250, verbose_name='شعار سال', null=True, blank=True)
    ostan = models.ForeignKey('cities_iran_manager_apps.Province', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='استان')

    essential_service_duration = models.CharField(max_length=250, null=True, blank=True, verbose_name='مدت خدمت ضرورت')
    Length_of_service_in_the_unit = models.CharField(max_length=250, null=True, blank=True,
                                                     verbose_name='مدت خدمت در یگان')
    annual_leave_quota = models.PositiveIntegerField("سقف مرخصی استحقاقی", default=0)
    incentive_leave_quota = models.PositiveIntegerField("سقف مرخصی تشویقی", default=0)
    sick_leave_quota = models.PositiveIntegerField("سقف مرخصی استعلاجی", default=0)
