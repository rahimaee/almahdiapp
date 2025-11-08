from django.db import models

class ExpiredReasonEnum(models.TextChoices):
    END_OF_SERVICE = "END_OF_SERVICE", "پایان خدمت"
    ESCAPE = "ESCAPE", "فرار"
    STUDY = "STUDY", "ادامه تحصیل"
    DEATH = "DEATH", "فوت"
    TRANSFER_DUTY = "TRANSFER_DUTY", "انتقال.پایان ماموریت"
    TRANSFER = "TRANSFER", "انتقال"
    DUTY = "DUTY", "ماموریت"
    EXPIRED = "EXPIRED", "منقضی از خدمت"


EXPIRED_REASON_CHOICES = ExpiredReasonEnum.choices

IMPORT_GROUP_FIELDS_EXCEL_CHOICES = [
    ("expired_file", "پرونده"),
    ("expired_file_number", "شماره پرونده"),
    ("national_code", "کد ملی"),
    ("birth_certificate_number", "شماره شناسنامه"),
    ("first_name", "نام"),
    ("last_name", "نام خانوادگی"),
    ("father_name", "نام پدر"),
    ("organization_code", "کد سربازی"),
    ("start_service_date", "تاریخ شروع خدمت"),
    ("runaway_date", "تاریخ فرار"),
    ("end_service_date", "تاریخ پایان خدمت"),
    ("settlement_date", "تاریخ تسویه"),
    ("expired_reason", "دلیل منقضی شدن"),
    ("review_status", "بررسی وضعیت"),
    ("status", "وضعیت"),
    ("description", "توضیحات"),
]

IMPORT_GROUP_FIELDS_EXCEL_FIELDS = [key for key, _ in IMPORT_GROUP_FIELDS_EXCEL_CHOICES]
IMPORT_GROUP_FIELDS_EXCEL_HEADERS = [value for _, value in IMPORT_GROUP_FIELDS_EXCEL_CHOICES]