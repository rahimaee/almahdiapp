from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import OrganizationalPosition
from soldires_apps.models import Soldier
from collections import defaultdict
from django.http import HttpResponse
from openpyxl import Workbook
from almahdiapp.utils.excel  import *
# ========================
#  فهرست جایگاه‌ها
# ========================
def organizational_position_index(request):
    """
    نمایش فهرست جایگاه‌ها و اطلاعات سربازان هر جایگاه
    """
    positions = OrganizationalPosition.objects.all().order_by('position_code')
    context = {
        'page_title': 'فهرست جایگاه‌های سازمانی',
        'description': 'لیست همه جایگاه‌های ثبت‌شده در سیستم',
        'positions': positions,
    }
    return render(request, 'pages/organizational_position_index.html', context)


# ========================
#  گزارش‌ها
# ========================
def organizational_position_reports(request):
    """
    نمایش گزارش‌های آماری جایگاه‌ها
    """
    context = {
        'page_title': 'گزارش جایگاه‌ها',
        'description': 'نمایش گزارش‌های آماری و تحلیلی جایگاه‌های سازمانی',
        'total_positions': OrganizationalPosition.objects.count(),
        'total_soldiers': Soldier.objects.count(),
    }
    return render(request, 'pages/organizational_position_reports.html', context)


# ========================
#  نمایش درخت سازمانی
# ========================
from .tree import build_organizational_tree

def organizational_position_tree(request):
    """
    نمایش ساختار درختی جایگاه‌ها بر اساس parent_group > group > position_code
    """
    positions = OrganizationalPosition.objects.all().order_by('position_group', 'position_code')
    tree = build_organizational_tree(positions)

    context = {
        'page_title': 'درخت سازمانی',
        'description': 'نمایش ساختار سلسله‌مراتبی جایگاه‌ها (والد، گروه، جایگاه)',
        'tree': tree
    }
    return render(request, 'pages/organizational_position_tree.html', context)
# ========================
#  درون‌ریزی جایگاه‌ها
# ========================
from .constants import *
from .enums import *
from almahdiapp.utils.builder import *
def organizational_position_import_data(request):
    """
    درون‌ریزی جایگاه‌ها از فایل CSV/Excel یا داده‌ی مستقیم
    """
    result = None
    if request.method == 'POST':
        excel_file = request.FILES.get("file")
        importer = ExcelImport(file=excel_file, choices=ORGANIZATIONAL_POSITION_CHOICES)
        
        importer.read_file()        # داده را بخوان
        importer.clean_data()       # اگر بخواهی تمیزکاری انجام شود
        
        records = importer.records  # لیست دیکشنری‌ها
        result = OrganizationalPosition.import_data(records)
        message = f"درون‌ریزی انجام شد. {result['created']} جدید، {result['updated']} بروزرسانی شد."
        messages.success(request, message)

    context = {
        'page_title': 'درون‌ریزی داده‌ها',
        'description': 'درون‌ریزی جایگاه‌های سازمانی از فایل CSV یا Excel',
        'result': result,
    }
    return render(request, 'pages/organizational_position_import_data.html', context)

def organizational_position_import_data_sample(request):
    """
    دانلود فایل نمونه جایگاه‌های سازمانی با استایل و سلول‌های الزامی
    """
    filename="نمونه_جایگاه_سازمانی.xlsx"
    headers = ORGANIZATIONAL_POSITION_HEADERS
    required_fields = [OrganizationalPositionField.POSITION_CODE.label]
    data = [
        [row.get(field, "") for field in ORGANIZATIONAL_POSITION_KEYS]
        for row in ORGANIZATIONAL_POSITION_SAMPLE
    ]
    exporter = ExcelExporter(
        headers=headers, 
        data=data, 
        required_fields=required_fields, 
    )
    bio = exporter.export_to_bytes()
    response = ExcelExporter.response(bio,filename)

    return response
# ========================
#  درون‌ریزی تخصیص سربازان
# ========================
def organizational_position_import_assign(request):
    """
    تخصیص سربازان به جایگاه‌ها از فایل داده
    """
    eb = EnumMetaBuilder(OrganizationalPositionAssignEnum)
    
    result = None
    if request.method == 'POST':
        excel_file = request.FILES.get("file")
        importer = ExcelImport(file=excel_file, choices=eb.choices)
        
        importer.read_file()        
        importer.clean_data()       
        
        records = importer.records
        result = OrganizationalPosition.assign_soldiers(records)
        messages.success(request, f"{result['assigned']} سرباز با موفقیت تخصیص داده شدند.")

    context = {
        'page_title': 'درون‌ریزی تخصیص',
        'description': 'درون‌ریزی تخصیص سربازان به جایگاه‌ها از فایل داده',
        'result': result,
    }
    return render(request, 'pages/organizational_position_import_assign.html', context)

def organizational_position_import_assign_sample(request):
    eb = EnumMetaBuilder(OrganizationalPositionAssignEnum)
    filename="تخصیص جایگاه سازمانی - سرباز.xlsx"
    required_fields = [
        OrganizationalPositionAssignEnum.NATIONAL_CODE.label,
        OrganizationalPositionAssignEnum.POSITION_CODE.label,
    ]
    data = [
        [row.get(field, "") for field in eb.keys]
        for row in ORGANIZATIONAL_POSITION_ASSIGN_SAMPLE
    ]
    exporter = ExcelExporter(
        headers=eb.headers, 
        data=data, 
        required_fields=required_fields, 
    )
    bio = exporter.export_to_bytes()
    response = ExcelExporter.response(bio,filename)

    return response

# ========================
#  برون‌ریزی جایگاه‌ها با جزئیات سرباز
# ========================
def organizational_position_export_data(request):
    """
    خروجی Excel از جایگاه‌های سازمانی با جزئیات سرباز.
    query param:
        status = "full" | "empty" | "all"
    """
    filename = "export_positions.xlsx"
    status = request.GET.get("status", "all").lower()

    positions = OrganizationalPosition.objects.all()

    if status == "full":
        positions = [p for p in positions if hasattr(p, "soldiers") and p.soldiers.exists()]
    elif status == "empty":
        positions = [p for p in positions if not hasattr(p, "soldiers") or not p.soldiers.exists()]
    # else: all positions

    data = []

    for pos in positions:
        soldiers = pos.soldiers.all() if hasattr(pos, "soldiers") else []
        soldiers_count = soldiers.count()

        if soldiers_count > 0:
            for soldier in soldiers:
                row = {f.label: getattr(pos, f.key, "") for f in OrganizationalPositionField}
                row.update({
                    "تعداد سربازان": soldiers_count,
                    "کد سازمانی سرباز": getattr(soldier.organizational_code, "code_number", ""),
                    "کد ملی سرباز": soldier.national_code,
                    "نام سرباز": soldier.first_name,
                    "نام خانوادگی": soldier.last_name,
                    "نام پدر": soldier.father_name,
                })
                data.append(row)
        else:
            # جایگاه خالی
            row = {f.label: getattr(pos, f.key, "") for f in OrganizationalPositionField}
            row.update({
                "تعداد سربازان": 0,
                "کد سازمانی سرباز": "",
                "کد ملی سرباز": "",
                "نام سرباز": "",
                "نام خانوادگی": "",
                "نام پدر": "",
            })
            data.append(row)

    # headers
    headers = [
    OrganizationalPositionField.POSITION_CODE.label,
    OrganizationalPositionField.POSITION_GROUP.label,
    ] + [
        "تعداد سربازان",
        "کد سازمانی سرباز",
        "کد ملی سرباز",
        "نام سرباز",
        "نام خانوادگی",
        "نام پدر",
    ]

    exporter = ExcelExporter(headers=headers, data=data)
    bio = exporter.export_to_bytes()
    response = ExcelExporter.response(bio, filename)
    return response

# ========================
#  برون‌ریزی تخصیص‌ها
# ========================
def organizational_position_export_assign(request):
    """
    خروجی Excel از تخصیص سربازان به جایگاه‌ها
    query params:
        is_checked: True/False/None برای فیلتر سربازان دارای جایگاه
    """
    filename = "export_position_assign.xlsx"
    is_checked = request.GET.get("is_checked")

    soldiers = Soldier.objects.filter(is_checked_out=False)
    if is_checked == "true":
        soldiers = soldiers.filter(position__isnull=False)
    elif is_checked == "false":
        soldiers = soldiers.filter(position__isnull=True)

    # ساختن لیست از Enum برای headers
    eb = EnumMetaBuilder(OrganizationalPositionAssignEnum)

    # داده‌ها
    data = []
    for soldier in soldiers:
        row = {
            # اطلاعات جایگاه
            "کد جایگاه": soldier.position.position_code if soldier.position else "",
           "جایگاه سازمانی": soldier.position.position_group if soldier.position else "",
            # اطلاعات سرباز
            "کد ملی سرباز": soldier.national_code,
            "نام سرباز": soldier.first_name,
            "نام خانوادگی": soldier.last_name,
            "نام پدر": soldier.father_name,
        }
        data.append(row)

    # headers
    headers = [
        "کد جایگاه",
        "جایگاه سازمانی",
        "کد ملی سرباز",
        "نام سرباز",
        "نام خانوادگی",
        "نام پدر",
    ]

    exporter = ExcelExporter(headers=headers, data=data)
    bio = exporter.export_to_bytes()
    response = ExcelExporter.response(bio, filename)
    return response
# ========================
#  پایگاه داده (پشتیبان‌گیری)
# ========================
from django.db.models import Q, Count

# ========================
#  پایگاه داده (پشتیبان‌گیری)
# ========================
def organizational_position_database(request):
    """
    مدیریت پایگاه داده جایگاه‌ها و سربازان
    """
    total_positions = OrganizationalPosition.objects.count()
    positions_without_title = OrganizationalPosition.objects.filter(title__isnull=True).count()
    
    # سربازان
    soldiers_with_position = Soldier.objects.filter(position__isnull=False)
    soldiers_present_with_position = soldiers_with_position.filter(is_checked_out=True)
    soldiers_present_without_position = Soldier.objects.filter(is_checked_out=True, position__isnull=True)
    soldiers_without_position = Soldier.objects.filter(position__isnull=True)
    soldiers_total_with_position = soldiers_with_position.count()
    soldiers_total_without_position = soldiers_without_position.count()
    
    latest_update = OrganizationalPosition.objects.order_by('-updated_at').first()

    context = {
        'page_title': 'پایگاه داده',
        'description': 'مدیریت و پشتیبان‌گیری از پایگاه داده جایگاه‌های سازمانی',
        'total_positions': total_positions,
        'positions_without_title': positions_without_title,
        'soldiers_with_position': soldiers_total_with_position,
        'soldiers_without_position': soldiers_total_without_position,
        'soldiers_present_with_position': soldiers_present_with_position.count(),
        'soldiers_present_without_position': soldiers_present_without_position.count(),
        'latest_update': latest_update,
    }
    
    return render(request, 'pages/organizational_position_database.html', context)
