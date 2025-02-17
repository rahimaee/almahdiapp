# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Soldier, OrganizationalCode
from .forms import SoldierForm
from cities_iran_manager_apps.models import City, Province
from units_apps.models import ParentUnit, SubUnit
import jdatetime
from soldier_documents_apps.models import SoldierDocuments
from soldier_service_apps.models import SoldierService


def soldier_list(request):
    # دریافت تمامی سربازها
    soldiers = Soldier.objects.all()
    return render(request, 'soldires_apps/soldier_list.html', {'soldiers': soldiers})


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
                    post_data[field] = gregorian_date.strftime("%Y-%m-%d")
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
            except (current_parent_unit.DoesNotExist, ValueError):
                form.fields['current_sub_unit'].queryset = SubUnit.objects.none()
        # اعتبارسنجی و ذخیره فرم
        if form.is_valid():
            form_save = form.save()
            soldire_id = form_save.id
            find_soldire = Soldier.objects.filter(pk=soldire_id).first()
            doc = SoldierDocuments.objects.create(soldier_id=find_soldire.id)
            service = SoldierService()
            service.soldier = find_soldire
            marital_status = find_soldire.marital_status
            print(marital_status)
            number_of_children = find_soldire.number_of_children
            if marital_status == 'married':
                print("sssssssssss")
                service.reduction_spouse = 60
                if number_of_children > 0:
                    service.reduction_children = 30
                if number_of_children > 1:
                    service.reduction_children = 30 + 40
                if number_of_children > 2:
                    service.reduction_children = 30 + 40 + 50
            personal_code = OrganizationalCode.objects.filter(id=find_soldire.organizational_code.id).first()
            personal_code.is_active = True
            personal_code.save()
            service.save()
            return redirect("soldier_list")
    else:
        form = SoldierForm()

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
