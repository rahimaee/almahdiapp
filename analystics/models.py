import uuid
import os
from django.db import models
from django.utils.timezone import now
from units_apps.models import UnitHistory
from training_center_apps.models import TrainingCenter
from django_jalali.db import models as jmodels
from django.utils.deconstruct import deconstructible
from multiselectfield import MultiSelectField
import re
from django.utils import timezone
from django.conf import settings

# مسیر آپلود فایل‌ها
def upload_to_analyze(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(settings.MEDIA_ROOT,'analystics','eshraf', filename)


class EshrafAnalyze(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    date = models.DateField(verbose_name="تاریخ")
    description = models.TextField(verbose_name="توضیحات")
    period_choices = [
        ("سه ماهه اول", "سه ماهه اول"),
        ("سه ماهه دوم", "سه ماهه دوم"),
        ("سه ماهه سوم", "سه ماهه سوم"),
        ("سه ماهه چهارم", "سه ماهه چهارم"),
    ]
    RENAME_FILE_LABEL = {
      "file_1": "فرم سربازان جدید",
      "file_2": "گزارش تردد",
      "file_3": "آمار آموزشی",
      "file_4": "لیست نفرات",
      "file_5": "برنامه شیفت‌ها",
      "file_6": "گزارش تجهیزات",
      "file_7": "لیست حضور و غیاب",
      "file_8": "آمار خدمات",
      "file_9": "گزارش عملکرد",
      "file_10": "گزارش نهایی",
   }
    RENAME_FILE_NAME = {
         "file_1": "1004005031",
         "file_2": "1004005032",
         "file_3": "1004005090",
         "file_4": "1004005091",
         "file_5": "1004005092",
         "file_6": "1004005093",
         "file_7": "1004005094",
         "file_8": "1004005095",
         "file_9": "1004005096",
         "file_10": "1004005097",
    }
    period = models.CharField(max_length=20, choices=period_choices, verbose_name="دوره")
    
    # فایل‌ها
    file_1 = models.FileField(upload_to=upload_to_analyze, blank=True, null=True, verbose_name='فایل 1')
    file_2 = models.FileField(upload_to=upload_to_analyze, blank=True, null=True, verbose_name='فایل 2')
    file_3 = models.FileField(upload_to=upload_to_analyze, blank=True, null=True, verbose_name='فایل 3')
    file_4 = models.FileField(upload_to=upload_to_analyze, blank=True, null=True, verbose_name='فایل 4')
    file_5 = models.FileField(upload_to=upload_to_analyze, blank=True, null=True, verbose_name='فایل 5')
    file_6 = models.FileField(upload_to=upload_to_analyze, blank=True, null=True, verbose_name='فایل 6')
    file_7 = models.FileField(upload_to=upload_to_analyze, blank=True, null=True, verbose_name='فایل 7')
    file_8 = models.FileField(upload_to=upload_to_analyze, blank=True, null=True, verbose_name='فایل 8')
    file_9 = models.FileField(upload_to=upload_to_analyze, blank=True, null=True, verbose_name='فایل 9')
    file_10 = models.FileField(upload_to=upload_to_analyze, blank=True, null=True, verbose_name='فایل 10')

    class Meta:
        verbose_name = 'فایل اشراف'
        verbose_name_plural = 'فایل‌های اشراف'

    def __str__(self):
      return f"{self.title} - {self.date}"