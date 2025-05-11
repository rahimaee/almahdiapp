import json
from .models import Province, City  # مسیر دقیق اپلیکیشن خودتان را جایگزین کنید
from django.http import HttpResponse
from django.http import JsonResponse
# مسیر فایل‌های JSON
import os

app_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(app_dir, "json")

provinces_file = os.path.join(data_dir, "provinces.json")
cities_file = os.path.join(data_dir, "cities.json")


def import_provinces():
    with open(provinces_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        province, created = Province.objects.get_or_create(
            id=item["id"],
            defaults={
                "name": item["name"],
                "tel_prefix": item.get("tel_prefix", "")
            }
        )
        if created:
            print(f"استان {province.name} اضافه شد.")
        else:
            print(f"استان {province.name} قبلاً وجود داشت.")


def import_cities():
    with open(cities_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        try:
            province = Province.objects.get(id=item["province_id"])
            city, created = City.objects.get_or_create(
                id=item["id"],
                defaults={
                    "name": item["name"],
                    "province": province
                }
            )
            if created:
                print(f"شهر {city.name} اضافه شد.")
            else:
                print(f"شهر {city.name} قبلاً وجود داشت.")
        except Province.DoesNotExist:
            print(f"⚠️ استان با ID {item['province_id']} یافت نشد!")


def run(request):
    import_provinces()
    import_cities()
    return HttpResponse('"✅ اطلاعات با موفقیت وارد شد!"')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Province, City
from .forms import ProvinceForm, CityForm


def province_list(request):
    provinces = Province.objects.all()
    return render(request, "cities_iran_manager_apps/province_list.html", {"provinces": provinces})


def province_create(request):
    if request.method == "POST":
        form = ProvinceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("province_list")
    else:
        form = ProvinceForm()
    return render(request, "cities_iran_manager_apps/province_form.html", {"form": form})


def province_edit(request, pk):
    province = get_object_or_404(Province, pk=pk)
    if request.method == "POST":
        form = ProvinceForm(request.POST, instance=province)
        if form.is_valid():
            form.save()
            return redirect("province_list")
    else:
        form = ProvinceForm(instance=province)
    return render(request, "cities_iran_manager_apps/province_form.html", {"form": form})


def city_create(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("province_list")
    else:
        form = CityForm()
    return render(request, "cities_iran_manager_apps/city_form.html", {"form": form})


def city_list(request):
    # گرفتن همه استان‌ها همراه با شهرهای مرتبط
    provinces = Province.objects.all()

    return render(request, "cities_iran_manager_apps/city_list.html", {"provinces": provinces})


def city_edit(request, pk):
    city = get_object_or_404(City, pk=pk)  # گرفتن شیء شهر با pk
    if request.method == "POST":
        form = CityForm(request.POST, instance=city)  # فرم ویرایش
        if form.is_valid():
            form.save()
            return redirect('city_list')  # بعد از ویرایش به لیست شهرها برگرد
    else:
        form = CityForm(instance=city)

    return render(request, 'cities_iran_manager_apps/city_form.html', {'form': form, 'city': city})


def get_cities(request):
    province_id = request.GET.get("province_id")
    if province_id:
        cities = City.objects.filter(province_id=province_id).values("id", "name")
        return JsonResponse(list(cities), safe=False)
    return JsonResponse([], safe=False)
