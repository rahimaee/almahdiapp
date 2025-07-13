from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ClearanceLetter
from soldires_apps.models import Soldier, Settlement
from django.utils import timezone


@receiver(post_save, sender=ClearanceLetter)
def update_soldier_status_on_clearance_approval(sender, instance, created, **kwargs):
    """
    وقتی نامه تسویه‌حساب تایید می‌شود، وضعیت سرباز را تغییر می‌دهد و Settlement ایجاد می‌کند
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
        
        # ذخیره تغییرات سرباز
        soldier.save(update_fields=['status', 'is_checked_out'])
        
        # ایجاد Settlement برای سرباز (اگر قبلاً وجود نداشته باشد)
        settlement, created = Settlement.objects.get_or_create(
            soldier=soldier,
            defaults={
                'total_debt_rial': 0,  # مقدار اولیه صفر
                'current_debt_rial': 0,  # مقدار اولیه صفر
                'final_settlement_date': timezone.now().date(),
                'status': 'review',  # ← اینجا باید 'review' باشد
                'description': f'تسویه‌حساب بر اساس نامه {instance.letter_number} - {instance.get_reason_display()}'
            }
        )
        
        if created:
            # اگر Settlement جدید ایجاد شد، تاریخ ثبت را تنظیم کن
            settlement.final_settlement_date = timezone.now().date()
            settlement.save(update_fields=['final_settlement_date'])


@receiver(post_delete, sender=ClearanceLetter)
def restore_soldier_status_on_clearance_delete(sender, instance, **kwargs):
    """
    وقتی نامه تسویه‌حساب حذف می‌شود، وضعیت سرباز را به حین خدمت بازمی‌گرداند و Settlement را حذف می‌کند
    """
    soldier = instance.soldier
    
    # بازگرداندن وضعیت سرباز به حین خدمت
    soldier.status = 'حین خدمت'
    soldier.is_checked_out = False
    
    # حذف Settlement مربوطه (اگر وجود داشته باشد)
    try:
        settlement = soldier.settlement
        settlement.delete()
    except Settlement.DoesNotExist:
        pass  # اگر Settlement وجود نداشت، مشکلی نیست
    
    # ذخیره تغییرات
    soldier.save(update_fields=['status', 'is_checked_out']) 