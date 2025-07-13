from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ClearanceLetter
from soldires_apps.models import Soldier


@receiver(post_save, sender=ClearanceLetter)
def update_soldier_status_on_clearance_approval(sender, instance, created, **kwargs):
    """
    وقتی نامه تسویه‌حساب تایید می‌شود، وضعیت سرباز را تغییر می‌دهد
    """
    if not created and instance.status == 'تایید شده':
        soldier = instance.soldier
        
        # تغییر وضعیت سرباز بر اساس علت تسویه‌حساب
        if instance.reason == 'پایان خدمت':
            soldier.status = 'پایان خدمت'
        elif instance.reason == 'قبولی در دانشگاه':
            soldier.status = 'قبولی در دانشگاه'
        elif instance.reason == 'انتقال':
            soldier.status = 'انتقالی'
        elif instance.reason == 'معافیت دائم':
            soldier.status = 'پایان خدمت'
        
        # علامت‌گذاری تسویه‌حساب
        soldier.is_checked_out = True
        
        # ذخیره تغییرات
        soldier.save(update_fields=['status', 'is_checked_out'])


@receiver(post_delete, sender=ClearanceLetter)
def restore_soldier_status_on_clearance_delete(sender, instance, **kwargs):
    """
    وقتی نامه تسویه‌حساب حذف می‌شود، وضعیت سرباز را به حین خدمت بازمی‌گرداند
    """
    soldier = instance.soldier
    
    # بازگرداندن وضعیت سرباز به حین خدمت
    soldier.status = 'حین خدمت'
    soldier.is_checked_out = False
    
    # ذخیره تغییرات
    soldier.save(update_fields=['status', 'is_checked_out']) 