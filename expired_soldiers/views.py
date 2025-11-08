import os
import uuid
from io import BytesIO
from urllib.parse import quote

import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import (
    JsonResponse,
)
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView

from .models import ExpiredSoldier
from .forms import ExpiredSoldierFilterForm
from .enums import *
from .constants import *
from .helpers import ExpiredSoldierHelpers

class ExpiredSoldierListView(ListView):
    model = ExpiredSoldier
    template_name = "pages/expired_soldiers_index.html"
    context_object_name = "soldiers"
    paginate_by = 50  # تعداد آیتم در هر صفحه

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ExpiredSoldierFilterForm(self.request.GET)

        if form.is_valid():
            search = form.cleaned_data.get("search")
            settlement_reason = form.cleaned_data.get("settlement_reason")
            end_service_start = form.cleaned_data.get("end_service_start")
            end_service_end = form.cleaned_data.get("end_service_end")
            settlement_start = form.cleaned_data.get("settlement_start")
            settlement_end = form.cleaned_data.get("settlement_end")

            if search:
                queryset = queryset.filter(
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search) |
                    Q(national_code__icontains=search)
                )
            if settlement_reason:
                queryset = queryset.filter(settlement_reason=settlement_reason)
            if end_service_start:
                queryset = queryset.filter(end_service_date__gte=end_service_start)
            if end_service_end:
                queryset = queryset.filter(end_service_date__lte=end_service_end)
            if settlement_start:
                queryset = queryset.filter(settlement_date__gte=settlement_start)
            if settlement_end:
                queryset = queryset.filter(settlement_date__lte=settlement_end)

        return queryset.order_by("-settlement_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ارسال فرم به template
        context['filter_form'] = ExpiredSoldierFilterForm(self.request.GET)
        return context


def api_expired_soldiers_search(request):
    query = request.GET.get('query', '')
    count = request.GET.get('count', 10)

    soldiers = ExpiredSoldier.search(query, count)

    data = list(soldiers.values(
        'id',
        'first_name',
        'last_name',
        'national_code',
        'father_name',
        'expired_file_number',
        'settlement_date',
    ))

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})



UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, "soldiers", "expired")
from datetime import datetime
import jdatetime

def expired_soldiers_import_group(request):
    """
    صفحه بارگذاری گروهی سربازان منقضی خدمت
    """
    # لیست فایل‌ها در پوشه
    
    files = ExpiredSoldierHelpers().files
    processing_files = [f for f in files if f['is_processing']]
    has_processing = len(processing_files) > 0
    context = {
        'has_processing':has_processing,
        "files": files,
        'processing_files':processing_files,
        'EXPIRED_REASON_CHOICES':EXPIRED_REASON_CHOICES
    }
    return render(request, "pages/expired_soldiers_import_group.html", context)


def expired_soldiers_import_group_upload(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # گرفتن نام فایل از input کاربر
        input_name = request.POST.get("filename", "").strip()

        # نام پایه فایل
        if input_name:
            base_name = input_name.strip()
        else:
            # بدون پسوند
            base_name, ext = os.path.splitext(file.name)
            base_name = base_name

        # پسوند فایل
        ext = os.path.splitext(file.name)[1]
        unique_filename = f"{base_name}__{uuid.uuid4().hex}{ext}".strip()

        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # ذخیره فایل
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        file_url = os.path.join(settings.MEDIA_URL, "soldiers", "expired", unique_filename)

        return JsonResponse({"success": True, "filename": unique_filename, "url": file_url})

    return JsonResponse({"success": False}, status=400)

from almahdiapp.utils.excel import ExcelExporter
def expired_soldiers_import_group_sample_excel(request):
    """
    تولید و ارسال یک فایل نمونه Excel (xlsx) برای ایمپورت گروهی سربازان.
    - شیت در حالت RTL قرار می‌گیرد.
    - ستون‌های الزامی (کد ملی، نام، نام خانوادگی) هایلایت شده‌اند.
    - شامل یک ردیف نمونه با داده‌های نمایشی است.
    """
    headers = IMPORT_GROUP_FIELDS_EXCEL_HEADERS

    rows = [
        [row.get(field, "") for field in IMPORT_GROUP_FIELDS_EXCEL_HEADERS] 
        for row in IMPORT_GROUP_SAMPLE_OBJ
    ]

    required_fields_key = ["first_name", "last_name"]
    
    required_fields = [
        value for key,value in IMPORT_GROUP_FIELDS_EXCEL_CHOICES
        if key in required_fields_key
    ]
    
    filename = "نمونه-واردسازی-سربازان.xlsx"

    exporter = ExcelExporter(
        headers=headers,
        data=rows,
        required_fields=required_fields,
    )
    
    bio = exporter.export_to_bytes()
    
    response = exporter.response(bio,filename)

    return response


def expired_soldiers_import_group_process_uploaded(request):
    pass


def expired_soldiers_import_group_action(request):
    """
    این تابع مسئول انجام عملیات مختلف بر روی فایل‌های آپلودشده‌ی مربوط به سربازان منقضی‌شده است.  
    این عملیات شامل سه بخش اصلی است:

    1. **دانلود (download):**
       - در صورتی که کاربر دکمه‌ی «دانلود» را بزند، فایل موردنظر از مسیر ذخیره‌شده خوانده می‌شود
         و با استفاده از پاسخ `FileResponse` به مرورگر ارسال می‌گردد تا کاربر بتواند آن را دریافت کند.
       - در صورت موفقیت، پیام مناسب به کاربر نمایش داده می‌شود.

    2. **حذف (delete):**
       - در صورتی که کاربر دکمه‌ی «حذف» را بزند، فایل موردنظر از سیستم فایل (در پوشه‌ی `media/uploads/expired_soldiers/`)
         حذف می‌شود.
       - پس از حذف موفقیت‌آمیز، پیام تأیید حذف نمایش داده می‌شود.
       - اگر فایل وجود نداشته باشد یا حذف با خطا مواجه شود، پیام خطا به کاربر نشان داده می‌شود.

    3. **پردازش (process):**
       - در صورتی که کاربر دکمه‌ی «پردازش» را بزند، سیستم فایل موردنظر را برای پردازش آماده می‌کند.
       - در این بخش می‌توان عملیات مختلفی انجام داد (مثلاً خواندن محتوای فایل، استخراج اطلاعات از Excel یا CSV،
         و ذخیره داده‌ها در پایگاه داده).
       - در حال حاضر تنها پیام موفقیت نمایش داده می‌شود، اما محل مناسبی برای افزودن منطق پردازش واقعی در نظر گرفته شده است.

    ⚙️ نکات فنی:
    - قبل از انجام هر عملیات، بررسی می‌شود که فایل واقعاً در مسیر ذخیره‌شده وجود دارد.
    - در صورت بروز هرگونه خطا (مثلاً فایل پیدا نشود یا دسترسی محدود باشد)،
      پیام خطا به کاربر نشان داده می‌شود.
    - در پایان، کاربر به صفحه‌ی اصلی مربوط به مدیریت گروه فایل‌های سربازان منقضی‌شده (`expired_soldiers_import_group`) بازگردانده می‌شود.
    """
    if request.method == "POST":
        filename = request.POST.get("filename")
        action_type = request.POST.get("action_type")
        file_path = os.path.join(UPLOAD_DIR, filename)

        # بررسی وجود فایل
        if not os.path.exists(file_path):
            messages.error(request, f"فایل {filename} یافت نشد.")
            return redirect('expired_soldiers_import_group')

        try:
        # دانلود فایل
            if action_type == "download":
                response = ExpiredSoldierHelpers.download_file(filename)
                messages.success(request, f"فایل {filename} دانلود شد.")
                return response
        # حذف فایل از سیستم
            elif action_type == "delete":
                is_removed = ExpiredSoldierHelpers.remove_file(filename)
                messages.success(request, f"فایل {filename} با {'موفقیت حذف شد' if is_removed else 'خطا مواجه شد.'}.")
        # پردازش فایل (اینجا نمونه نمایشی است)
        # تو می‌توانی در اینجا کد واقعی پردازش فایل (مثلاً خواندن CSV یا Excel) را بنویسی.
            elif action_type == "process":
                ExpiredSoldierHelpers.import_group_from_excel(filename)
                messages.success(request, f"فایل {filename} با موفقیت پردازش شد.")
            else:
                messages.error(request, "اکشن نامعتبر است.")

        except Exception as e:
            messages.error(request, f"خطا در انجام عملیات: {e}")

    return redirect('expired_soldiers_import_group')

from django.http import JsonResponse
from .tasks import ProcessingManager
from django.forms.models import model_to_dict
import math
from django.forms.models import model_to_dict
from django.http import JsonResponse

def clean_json_value(value):
    """
    پاک‌سازی مقدارها برای تبدیل امن به JSON
    """
    if isinstance(value, float) and math.isnan(value):
        return None
    elif isinstance(value, dict):
        return {k: clean_json_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [clean_json_value(v) for v in value]
    elif hasattr(value, "__dict__"):
        return model_to_dict(value)
    elif isinstance(value, Exception):
        return str(value)
    else:
        return value
    
def expired_soldiers_task_active(request):
    """
    بازگرداندن وضعیت فایل‌های در حال پردازش به صورت JSON ایمن
    """
    tasks = ProcessingManager.list_processing_tasks()  # لیست دیکشنری‌ها
    safe_tasks = []

    for t in tasks:
        # پاک‌سازی داده‌ها برای جلوگیری از خطای JSON
        safe_task = {
            "filename": clean_json_value(t.get("filename", "")),
            "status": clean_json_value(t.get("status", "")),
            "task_id": clean_json_value(t.get("task_id", "")),
            "processed_count": clean_json_value(t.get("processed_count", 0)),
            "error_count": clean_json_value(t.get("error_count", 0)),
            "total_count": clean_json_value(t.get("total_count", 0)),
            "finished": clean_json_value(t.get("finished", False)),
            "last_processed": clean_json_value(t.get("last_processed", [])),
        }
        safe_tasks.append(safe_task)

    # می‌تونی در همینجا تسک‌های تمام‌شده را هم پاک کنی:
    # ProcessingManager.clean_finished_tasks()

    return JsonResponse(safe_tasks, safe=False)


import os
from django.db import connection
from django.shortcuts import render
from .models import ExpiredSoldier


def expired_soldiers_manage_database(request):
    """
    نمایش اطلاعات مدیریتی دیتابیس سربازان منقضی خدمت (فقط با GET)
    """
    # تعداد رکوردها
    total_count = ExpiredSoldier.objects.count()

    # اندازه فایل یا جدول دیتابیس
    size_bytes = 0
    db_engine = connection.settings_dict["ENGINE"]

    try:
        with connection.cursor() as cursor:
            if "sqlite" in db_engine:
                db_file = connection.settings_dict["NAME"]
                if os.path.exists(db_file):
                    size_bytes = os.path.getsize(db_file)
            elif "postgresql" in db_engine:
                cursor.execute("SELECT pg_total_relation_size('expired_soldiers_expiredsoldier');")
                size_bytes = cursor.fetchone()[0]
    except Exception:
        pass

    # تبدیل به MB
    size_mb = round(size_bytes / (1024 * 1024), 2)

    # شمارش رکوردهای خاص (مثلاً دارای خطا یا خالی)
    recent_records = ExpiredSoldier.objects.filter()[:10]  # آخرین رکوردها
    empty_records_sq = ExpiredSoldier.objects.filter(first_name="", last_name="")
    empty_records = empty_records_sq.count()
    empty_records_list = empty_records_sq[:10]  

    # اطلاعات سیستم (در صورت نیاز)
    db_path = connection.settings_dict.get("NAME", "")
    db_exists = os.path.exists(db_path)
    db_modified = os.path.getmtime(db_path) if db_exists else None

    context = {
        "total_count": total_count,
        "size_mb": size_mb,
        "db_path": db_path,
        "db_exists": db_exists,
        "empty_records": empty_records,
        "recent_records": recent_records,
        "db_modified": db_modified,
        "empty_records_list":empty_records_list
    }

    return render(request, "pages/expired_soldiers_manage_database.html", context)
