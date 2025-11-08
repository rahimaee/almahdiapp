import os
import uuid
from datetime import datetime
import jdatetime
from django.conf import settings
from django.http import FileResponse
from django.contrib import messages
from .enums import (
    IMPORT_GROUP_FIELDS_EXCEL_CHOICES,
    IMPORT_GROUP_FIELDS_EXCEL_FIELDS,
    IMPORT_GROUP_FIELDS_EXCEL_HEADERS,
    EXPIRED_REASON_CHOICES
)
from .models import ExpiredSoldier
import pandas as pd
from django.db import models
from django.contrib.auth import get_user_model
from .tasks import *

class ExpiredSoldierHelpers:
    UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, "soldiers", "expired")
    IMPORT_GROUP_FIELDS_EXCEL_CHOICES = IMPORT_GROUP_FIELDS_EXCEL_CHOICES
    IMPORT_GROUP_FIELDS_EXCEL_FIELDS = IMPORT_GROUP_FIELDS_EXCEL_FIELDS
    IMPORT_GROUP_FIELDS_EXCEL_HEADERS = IMPORT_GROUP_FIELDS_EXCEL_HEADERS
    EXPIRED_REASON_CHOICES = EXPIRED_REASON_CHOICES
    
    @classmethod
    def exist_file(cls, filename):
        """
        بررسی وجود فایل در مسیر ذخیره‌سازی.
        اگر فایل وجود داشته باشد مسیر کاملش را برمی‌گرداند، در غیر این صورت False.
        """
        file_path = os.path.join(cls.UPLOAD_DIR, filename)
        return file_path if os.path.exists(file_path) else False

    @classmethod
    def save_file(cls, uploaded_file, input_name=None):
        """
        ذخیره فایل Excel آپلود شده در مسیر UPLOAD_DIR.
        اگر input_name داده شود، از آن به‌عنوان نام فایل استفاده می‌شود.
        در غیر این صورت نام فایل اصلی آپلود شده استفاده خواهد شد.
        """
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)

        # نام پایه
        if input_name:
            base_name = input_name.strip()
        else:
            base_name, _ = os.path.splitext(uploaded_file.name)

        ext = os.path.splitext(uploaded_file.name)[1]
        unique_filename = f"{base_name}__{uuid.uuid4().hex}{ext}".strip()
        file_path = os.path.join(cls.UPLOAD_DIR, unique_filename)

        # ذخیره فایل
        with open(file_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        file_url = os.path.join(settings.MEDIA_URL, "soldiers", "expired", unique_filename)
        return {"filename": unique_filename, "url": file_url, "path": file_path}

    @classmethod
    def remove_file(cls, filename):
        """
        حذف فایل از مسیر ذخیره‌سازی
        """
        file_path = os.path.join(cls.UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    @classmethod
    def download_file(cls, filename):
        """
        برگرداندن FileResponse برای دانلود فایل مورد نظر
        """
        file_path = os.path.join(cls.UPLOAD_DIR, filename)
        if not os.path.exists(file_path):
            return None
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)

    @classmethod
    def import_group_from_excel(cls, filename):
        """
        خواندن داده‌ها از فایل Excel و افزودن اطلاعات در دیتابیس.
        """
        if not cls.exist_file(filename):
            raise FileNotFoundError(f"فایل {filename} یافت نشد.")

        file_path = os.path.join(cls.UPLOAD_DIR, filename)

        # خواندن داده‌ها از فایل اکسل
        df = pd.read_excel(file_path, sheet_name=0, dtype=str)  # همه ستون‌ها به رشته تبدیل شوند

        # ستون‌هایی که باید حتما رشته باشند و صفرهای پیشرو حفظ شود
        cols_to_str = ["national_code", "birth_certificate_number", "expired_file_number"]
        for col in cols_to_str:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: str(x).strip() if pd.notna(x) else "")

        # حذف ردیف‌های کاملاً خالی
        df.dropna(how="all", inplace=True)

        # trim کردن همه مقادیر متنی
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.strip()

        # تبدیل LIST از IMPORT_GROUP_FIELDS_EXCEL_CHOICES به دیکشنری برای دسترسی بهتر
        choices_dict = dict(cls.IMPORT_GROUP_FIELDS_EXCEL_CHOICES)
        # تبدیل فارسی به کلیدهای معادل
        swapped_choices_dict = {v: k for k, v in choices_dict.items()}

        # تغییر نام ستون‌ها از فارسی به کلیدهای مدل
        df.columns = [swapped_choices_dict.get(col, col) for col in df.columns]

        # تبدیل به لیست از دیکشنری‌ها
        records = df.to_dict(orient="records")

        # شروع پردازش با filename به عنوان task_id
        task_id = ProcessingManager.start_processing(filename, records)

        # حالا می‌توانیم وضعیت task را با task_id دنبال کنیم
        status = ProcessingManager.get_task_status(filename)
        return status
    
    @classmethod
    def export_group_excel(cls, queryset=None):
        """
        خروجی گرفتن از داده‌های سربازان منقضی خدمت به فایل Excel
        """
        if queryset is None:
            queryset = ExpiredSoldier.objects.all()

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Expired Soldiers"

        # نوشتن هدرها
        sheet.append(cls.IMPORT_GROUP_FIELDS_EXCEL_HEADERS)

        # نوشتن داده‌ها
        for soldier in queryset:
            row = []
            for field in cls.IMPORT_GROUP_FIELDS_EXCEL_FIELDS:
                value = getattr(soldier, field, "")
                row.append(value)
            sheet.append(row)

        # تنظیم راست‌به‌چپ
        sheet.sheet_view.rightToLeft = True

        # ذخیره در حافظه
        output_filename = f"expired_soldiers_export_{uuid.uuid4().hex[:8]}.xlsx"
        output_path = os.path.join(cls.UPLOAD_DIR, output_filename)
        workbook.save(output_path)

        return {
            "filename": output_filename,
            "path": output_path,
            "url": os.path.join(settings.MEDIA_URL, "soldiers", "expired", output_filename),
        }

    @property
    def files(self):
        """
        بازگرداندن لیست فایل‌های موجود در پوشه‌ی UPLOAD_DIR به همراه جزئیات هرکدام.
        """
        files = []
        if os.path.exists(self.UPLOAD_DIR):
            for f in os.listdir(self.UPLOAD_DIR):
                path = os.path.join(self.UPLOAD_DIR, f)
                if os.path.isfile(path):
                    created_timestamp = os.path.getctime(path)
                    gregorian_datetime = datetime.fromtimestamp(created_timestamp)
                    created_at = jdatetime.datetime.fromgregorian(datetime=gregorian_datetime)
                    # بررسی وضعیت پردازش فایل
                    task_id = ProcessingManager.get_task_id(f)
                    is_processing = True if task_id else False
                    base_name, ext = os.path.splitext(f)
                    
                    is_finished = ProcessingManager.get_task_finished(f)
                    
                    if is_finished:
                        is_processing= False
                        task_id=False
                        
                    files.append({
                        "base_name": base_name.strip(),
                        "ext": ext.strip(),
                        "filename": f.strip(),
                        "path": path,
                        "url": os.path.join(settings.MEDIA_URL, "soldiers", "expired", f),
                        "created_at": created_timestamp,
                        "created_at_display": created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "is_processing": is_processing,
                        "task_id": task_id
                    })

            files.sort(key=lambda x: x['created_at'], reverse=True)

        return files
