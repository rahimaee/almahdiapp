
# ------------------------------------------------------------------------
# Notes & Example Usage (در قالب کامنت)
# ------------------------------------------------------------------------

# مثال چگونگی استفاده ساده:
# 1) یک GuardConfig بساز:
#    cfg = GuardConfig.objects.create(
#        name="نسخه پایلوت",
#        default_entry_start=time(6,0),
#        default_entry_end=time(8,0),
#        default_exit_start=time(13,0),
#        default_exit_end=time(14,0),
#        penalty_policy={
#            "penalties": [
#                {"type": "restriction", "per_minute": 30, "restriction_minutes": 60},
#                {"type": "points", "per_minute": 60, "points": -5}
#            ],
#            "absence": {"type": "points", "points": -20}
#        }
#    )
#
# 2) قواعد برای روزهای هفته اضافه کن:
#    GuardRule.objects.create(config=cfg, weekday=0, entry_start=time(6,0), entry_end=time(8,0), exit_start=time(13,0), exit_end=time(14,0))
#
# 3) هنگام ثبت ورود/خروج:
#    att = Attendance.objects.create(soldier=soldier, date=date.today(), actual_entry=time(8,0))
#    result = att.finalize_and_save(config=cfg)
#    # result شامل applied_penalty و جزییات محاسبه است.
#
# نکات:
# - برای پردازش دسته‌ای (مثلاً هر روز نیمه‌شب) یک task ایجاد کن که برای همهٔ Attendance های آن روز apply_rules_and_compute را اجرا کند.
# - اگر می‌خواهی خلاصهٔ سریع از سربازها که در X روز آینده پایان خدمت دارند بگیری، از فیلدهای soldier.service_end_date استفاده کن.
#
# Migration / Indexing:
# - برای queryهای تاریخی، اضافه کردن BrinIndex روی date کمک بزرگی می‌کند (که در meta مدل Attendance آمده).
#
# Extendability:
# - برای پشتیبانی از rrule، می‌توان فیلد rrule_string به GuardRule افزود و از کتابخانه dateutil.rrule برای محاسبه occurrenceها بهره برد.
# - برای گزارش‌های complex، یک view یا materialized view در دیتابیس بساز که گزارش‌های روزانه/ماهانه را نگه دارد.
#
# Security:
# - مطمئن شو فایل‌های audit و action توسط کاربران بدون دسترسی نمایش داده نمی‌شوند.
# - داده‌های حساس مثل national_code را در سطح UI/permissions محافظت کن.
#
# Final note:
# - این طراحی طوری است که می‌توان در آینده انواع جدیدی از actions (مثل جریمه مالی، فراخوانی webhook، ارسال پیامک) به سادگی اضافه کرد؛
#   کافی‌ست یک action جدید به RewardPenalty.ACTION_CHOICES اضافه و handler آن را در لایه سرویس پیاده‌سازی کنی.
