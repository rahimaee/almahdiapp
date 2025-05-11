# views.py
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Soldier, OrganizationalCode
from .forms import SoldierForm, SoldierSearchForm, SoldierPhotoForm, PhotoZipUploadForm
from cities_iran_manager_apps.models import City, Province
from units_apps.models import ParentUnit, SubUnit
import jdatetime
from soldier_documents_apps.models import SoldierDocuments
from soldier_service_apps.models import SoldierService
from apps_settings.models import AppsSettings
import zipfile
import os
from io import BytesIO
from django.shortcuts import render
from django.core.files.base import ContentFile
from .models import Soldier
from .forms import PhotoZipUploadForm
from datetime import date


def soldier_list(request):
    form = SoldierSearchForm(request.GET or None)
    soldiers = Soldier.objects.all().select_related(
        'residence_province',
        'residence_city',
        'current_parent_unit',
        'current_sub_unit',
        'basic_training_center'
    )

    if form.is_valid():
        data = form.cleaned_data

        # ساخت کوئری پویا
        query = Q()

        # فیلدهای متنی
        text_fields = [
            'national_code', 'first_name', 'last_name', 'father_name',
            'organizational_code', 'id_card_code', 'birth_place',
            'issuance_place', 'health_status_description'
        ]
        for field in text_fields:
            if value := data.get(field):
                query &= Q(**{f"{field}__icontains": value})

        # فیلدهای رابطه‌ای
        relation_fields = [
            'residence_province', 'residence_city',
            'current_parent_unit', 'current_sub_unit',
            'basic_training_center'
        ]
        for field in relation_fields:
            if value := data.get(field):
                query &= Q(**{field: value})

        # فیلدهای انتخابی
        choice_fields = [
            'rank', 'health_status', 'blood_group',
            'degree', 'skill_certificate', 'skill_group',
            'has_driving_license', 'marital_status'
        ]
        for field in choice_fields:
            if value := data.get(field):
                query &= Q(**{field: value})

        # فیلدهای عددی
        numeric_fields = [
            'training_duration', 'essential_service_duration',
            'number_of_children', 'number_of_certificates'
        ]
        for field in numeric_fields:
            if value := data.get(field):
                query &= Q(**{field: value})

        # فیلدهای تاریخی
        date_fields = ['service_entry_date', 'dispatch_date', 'birth_date']
        for field in date_fields:
            value = data.get(field)
            if value:
                try:
                    # تبدیل تاریخ شمسی به میلادی
                    year, month, day = map(int, value.split('/'))
                    gregorian_date = jdatetime.date(year, month, day).togregorian()

                    # جستجو در دیتابیس بر اساس تاریخ میلادی
                    # مقایسه تاریخ‌ها با استفاده از __gte و __lte
                    query &= Q(**{f"{field}__gte": gregorian_date})  # تاریخ بزرگتر یا مساوی
                    query &= Q(**{f"{field}__lte": gregorian_date})  # تاریخ کوچکتر یا مساوی
                except (ValueError, TypeError):
                    pass  # اگر تاریخ به درستی تبدیل نشد، از آن عبور کن

        # فیلدهای بولی
        bool_fields = [
            'is_guard_duty', 'independent_married', 'is_certificate'
        ]
        for field in bool_fields:
            if value := data.get(field):
                query &= Q(**{field: value})

        soldiers = soldiers.filter(query)

    return render(request, 'soldires_apps/soldier_list.html', {
        'form': form,
        'soldiers': soldiers
    })


def convert_jalali_to_gregorian_string(jalali_str):
    """تبدیل رشته تاریخ شمسی به رشته میلادی به فرمت YYYY-MM-DD"""
    try:
        parts = [int(part) for part in jalali_str.split('/')]
        j_date = jdatetime.date(*parts)
        g_date = j_date.togregorian()
        return g_date.strftime('%Y-%m-%d')
    except Exception as e:
        return None  # یا raise e


def soldier_create(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        # تبدیل تاریخ‌های شمسی به میلادی
        date_fields = ["birth_date", "dispatch_date", "service_entry_date"]
        for field in date_fields:
            date_value = post_data.get(field)
            if date_value:
                try:
                    year, month, day = map(int, date_value.split("/"))
                    gregorian_date = jdatetime.date(year, month, day).togregorian()
                    post_data[field] = gregorian_date.isoformat()  # تبدیل به فرمت تاریخ میلادی
                except ValueError:
                    pass

        # ایجاد فرم با داده‌های POST
        form = SoldierForm(post_data)

        # بروزرسانی queryset شهرها بر اساس استان انتخاب شده
        residence_province_id = post_data.get('residence_province')
        if residence_province_id:
            try:
                province = Province.objects.get(id=residence_province_id)
                form.fields['residence_city'].queryset = City.objects.filter(province=province)
            except (Province.DoesNotExist, ValueError):
                form.fields['residence_city'].queryset = City.objects.none()

        current_parent_unit_id = post_data.get('current_parent_unit')
        if current_parent_unit_id:
            try:
                current_parent_unit = ParentUnit.objects.get(id=current_parent_unit_id)
                form.fields['current_sub_unit'].queryset = SubUnit.objects.filter(parent_unit=current_parent_unit)
            except (ParentUnit.DoesNotExist, ValueError):
                form.fields['current_sub_unit'].queryset = SubUnit.objects.none()
        # اعتبارسنجی و ذخیره فرم
        if form.is_valid():
            form_save = form.save()
            soldire_id = form_save.id
            aps = AppsSettings.objects.first()
            find_soldire = Soldier.objects.filter(pk=soldire_id).first()
            doc = SoldierDocuments.objects.create(soldier_id=find_soldire.id)
            service = SoldierService()
            service.annual_leave_quota = aps.annual_leave_quota
            service.incentive_leave_quota = aps.incentive_leave_quota
            service.sick_leave_quota = aps.sick_leave_quota
            service.soldier = find_soldire
            marital_status = find_soldire.marital_status
            number_of_children = find_soldire.number_of_children
            if marital_status == 'married':
                service.reduction_spouse = 60
                if number_of_children > 0:
                    service.reduction_children = 90
                if number_of_children > 1:
                    service.reduction_children = 90 + 120
                if number_of_children > 2:
                    service.reduction_children = 90 + 120 + 150
            personal_code = OrganizationalCode.objects.filter(id=find_soldire.organizational_code.id).first()
            personal_code.is_active = True
            personal_code.save()
            service.save()
            return redirect("soldier_list")
    else:
        form = SoldierForm()
        aps = AppsSettings.objects.first()
        if aps is None:
            form.fields['essential_service_duration'].initial = 0
        else:
            form.fields['essential_service_duration'].initial = aps.essential_service_duration

    return render(request, "soldires_apps/soldier_create.html", {"form": form})


def soldier_detail(request, pk):
    # دریافت سرباز بر اساس primary key (pk)
    soldier = get_object_or_404(Soldier, pk=pk)
    return render(request, 'soldires_apps/soldier_detail.html', {'soldier': soldier})


def soldier_edit(request, pk):
    # دریافت سرباز بر اساس primary key (pk)
    soldier = get_object_or_404(Soldier, pk=pk)

    if request.method == "POST":
        form = SoldierForm(request.POST, instance=soldier)
        if form.is_valid():
            form.save()
            return redirect('soldier_detail', pk=soldier.pk)
    else:
        form = SoldierForm(instance=soldier)

    return render(request, 'soldires_apps/soldier_edit.html', {'form': form})


def upload_soldier_photo(request, soldier_id):
    soldier = get_object_or_404(Soldier, id=soldier_id)

    if request.method == 'POST':
        form = SoldierPhotoForm(request.POST, request.FILES, instance=soldier)
        if form.is_valid():
            form.save()
            return redirect('soldier_detail', pk=soldier.id)  # یا هر صفحه‌ای که می‌خواهی برگردد
    else:
        form = SoldierPhotoForm(instance=soldier)

    return render(request, 'soldires_apps/upload_photo.html', {'form': form, 'soldier': soldier})


def bulk_photo_upload(request):
    message = ""
    not_found = []  # کدملی‌هایی که پیدا نشدند
    uploaded = []  # کدملی‌هایی که موفق بودن

    if request.method == 'POST':
        form = PhotoZipUploadForm(request.POST, request.FILES)
        if form.is_valid():
            zip_file = request.FILES['zip_file']
            if zipfile.is_zipfile(zip_file):
                zip_data = zipfile.ZipFile(zip_file)
                for filename in zip_data.namelist():
                    if filename.endswith(('.jpg', '.jpeg', '.png')):
                        national_code = os.path.splitext(os.path.basename(filename))[0].strip()
                        try:
                            soldier = Soldier.objects.get(national_code=national_code)
                            image_data = zip_data.read(filename)
                            soldier.photo_scan.save(
                                filename,
                                ContentFile(image_data),
                                save=True
                            )
                            uploaded.append(national_code)
                        except Soldier.DoesNotExist:
                            not_found.append(national_code)
                message = "عملیات آپلود تمام شد."
            else:
                message = "فایل ZIP معتبر نیست."
    else:
        form = PhotoZipUploadForm()

    return render(request, 'soldires_apps/bulk_photo_upload.html', {
        'form': form,
        'message': message,
        'uploaded': uploaded,
        'not_found': not_found
    })
