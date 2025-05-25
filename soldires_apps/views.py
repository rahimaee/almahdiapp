# views.py
import datetime
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils import timezone
from datetime import timedelta
from soldire_letter_apps.models import NormalLetterMentalHealthAssessmentAndEvaluation, IntroductionLetter
from .models import Soldier, OrganizationalCode, Settlement, PaymentReceipt
from .forms import SoldierForm, SoldierSearchForm, SoldierPhotoForm, PhotoZipUploadForm, SoldierFormUpdate
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
from django.utils.timezone import now
from .models import UnitHistory
from django.db.models.fields.related import ForeignKey, OneToOneField


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
            # ایجاد معرفی نامه و 4 برگ
            my_in_letter = IntroductionLetter()
            my_in_letter.soldier = find_soldire
            my_in_letter.part = form.cleaned_data['current_parent_unit']
            my_in_letter.sub_part = form.cleaned_data['current_sub_unit']
            my_in_letter.letter_type = 'چهاربرگ+معرفی نامه'
            my_in_letter.save()
            # ایجاد نامه تست سلامت
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
    soldier = get_object_or_404(Soldier, pk=pk)

    if request.method == "POST":
        post_data = request.POST.copy()

        # تبدیل تاریخ‌ها
        date_fields = ["birth_date", "dispatch_date", "service_entry_date"]
        for field in date_fields:
            date_value = post_data.get(field)
            if date_value:
                try:
                    date_value = date_value.strip()
                    if '/' in date_value:
                        year, month, day = map(int, date_value.split("/"))
                        gregorian_date = jdatetime.date(year, month, day).togregorian()
                    else:
                        year, month, day = map(int, date_value.split("-"))
                        gregorian_date = date(year, month, day)
                    post_data[field] = gregorian_date
                except:
                    post_data[field] = getattr(soldier, field)

        # نگهداری مقادیر قبلی واحدها
        old_parent_unit = soldier.current_parent_unit
        old_sub_unit = soldier.current_sub_unit

        form = SoldierFormUpdate(post_data, instance=soldier)

        # وابستگی‌ها
        if post_data.get('residence_province'):
            try:
                province = Province.objects.get(id=post_data['residence_province'])
                form.fields['residence_city'].queryset = City.objects.filter(province=province)
            except:
                form.fields['residence_city'].queryset = City.objects.none()

        if post_data.get('current_parent_unit'):
            try:
                parent_unit = ParentUnit.objects.get(id=post_data['current_parent_unit'])
                form.fields['current_sub_unit'].queryset = SubUnit.objects.filter(parent_unit=parent_unit)
            except:
                form.fields['current_sub_unit'].queryset = SubUnit.objects.none()

        form.fields['organizational_code'].queryset = OrganizationalCode.objects.filter(
            Q(is_active=False) | Q(id=soldier.organizational_code.id)
        )

        if form.is_valid():
            updated_fields = {}
            for field_name in form.fields:
                updated_fields[field_name] = form.cleaned_data.get(field_name)

            for field, value in updated_fields.items():
                setattr(soldier, field, value)

            soldier.save()

            # ثبت تاریخچه اگر تغییر کرده باشد
            if old_parent_unit != soldier.current_parent_unit or old_sub_unit != soldier.current_sub_unit:
                last_history = soldier.unit_history.filter(end_date__isnull=True).last()
                if last_history:
                    last_history.end_date = now()
                    last_history.save()

                UnitHistory.objects.create(
                    soldier=soldier,
                    parent_unit=soldier.current_parent_unit,
                    sub_unit=soldier.current_sub_unit,
                    start_date=now(),
                )

            return redirect('soldier_detail', pk=soldier.pk)
        else:
            print("Form errors:", form.errors)

    else:
        form = SoldierFormUpdate(instance=soldier)

        if soldier.residence_province:
            form.fields['residence_city'].queryset = City.objects.filter(province=soldier.residence_province)
        if soldier.current_parent_unit:
            form.fields['current_sub_unit'].queryset = SubUnit.objects.filter(parent_unit=soldier.current_parent_unit)

        form.fields['organizational_code'].queryset = OrganizationalCode.objects.filter(
            Q(is_active=False) | Q(id=soldier.organizational_code.id)
        )

        # تاریخ‌های شمسی
        if soldier.birth_date:
            j = jdatetime.date.fromgregorian(date=soldier.birth_date)
            form.initial['birth_date'] = f"{j.year}/{str(j.month).zfill(2)}/{str(j.day).zfill(2)}"
        if soldier.dispatch_date:
            j = jdatetime.date.fromgregorian(date=soldier.dispatch_date)
            form.initial['dispatch_date'] = f"{j.year}/{str(j.month).zfill(2)}/{str(j.day).zfill(2)}"
        if soldier.service_entry_date:
            j = jdatetime.date.fromgregorian(date=soldier.service_entry_date)
            form.initial['service_entry_date'] = f"{j.year}/{str(j.month).zfill(2)}/{str(j.day).zfill(2)}"

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


def review_settlements(request):
    # گرفتن همه سربازهایی که نیاز به بررسی دارند
    settlements = Settlement.objects.filter(need_rights_recheck=True)

    if request.method == 'POST':
        # دریافت داده‌ها از فرم
        for settlement in settlements:
            # پیدا کردن سرباز و تغییر وضعیت
            new_debt = request.POST.get(f'debt_{settlement.id}')
            no_review = request.POST.get(f'no_review_{settlement.id}')

            if new_debt:
                settlement.current_debt_rial = int(new_debt)
                settlement.updated_at = datetime.datetime.now()
                settlement.save()
            if no_review:
                settlement.need_rights_recheck = False
                settlement.status = 'pending'  # تغییر وضعیت به "در انتظار تسویه"
                settlement.updated_at = datetime.datetime.now()

            settlement.save()

        return redirect('review_settlements')  # پس از ارسال فرم، مجدداً لیست را نشان می‌دهیم

    return render(request, 'soldires_apps/review_settlements.html', {'settlements': settlements})


def payment_receipt_create(request):
    # گرفتن همه سربازهایی که بدهی دارند
    settlements = Settlement.objects.filter(current_debt_rial__gt=0)

    if request.method == 'POST':
        # گرفتن اطلاعات از فرم
        settlement_id = request.POST.get('settlement_id')
        amount_rial = request.POST.get('amount_rial')
        receipt_number = request.POST.get('receipt_number')
        deposit_date = request.POST.get('deposit_date')
        bank_operator_code = request.POST.get('bank_operator_code')

        # پیدا کردن تسویه‌حساب سرباز انتخاب شده
        settlement = Settlement.objects.get(id=settlement_id)

        # ایجاد فیش واریزی
        PaymentReceipt.objects.create(
            settlement=settlement,
            amount_rial=amount_rial,
            receipt_number=receipt_number,
            deposit_date=deposit_date,
            bank_operator_code=bank_operator_code
        )
        return redirect('payment_receipt_create')  # پس از ثبت فیش، صفحه را دوباره بارگذاری می‌کنیم

    return render(request, 'soldires_apps/payment_receipt_create.html', {'settlements': settlements})


def soldiers_settlement_list(request):
    # گرفتن همه سربازانی که تسویه‌حساب دارند
    soldiers = Soldier.objects.all()

    # گرفتن اطلاعات تسویه‌حساب برای هر سرباز
    soldier_data = []
    for soldier in soldiers:
        settlement = soldier.settlement if hasattr(soldier, 'settlement') else None
        soldier_data.append({
            'soldier': soldier,
            'settlement': settlement
        })

    return render(request, 'soldires_apps/soldiers_settlement_list.html', {'soldier_data': soldier_data})


def settlement_payments_view(request, settlement_id):
    settlement = get_object_or_404(Settlement, id=settlement_id)
    payments = settlement.payments.all().order_by('-deposit_date')  # آخرین‌ها اول
    return render(request, 'soldires_apps/settlement_payments.html', {
        'settlement': settlement,
        'payments': payments,
    })


from django.db.models import OuterRef, Subquery, Max


def due_mental_health_letters(request):
    six_months_ago = timezone.now() - timedelta(days=180)

    # آخرین تست هر سرباز
    latest_letters = NormalLetterMentalHealthAssessmentAndEvaluation.objects.values(
        'normal_letter__soldier'
    ).annotate(
        latest_date=Max('created_at')
    ).filter(
        latest_date__lte=six_months_ago
    )

    # گرفتن آی‌دی سربازهایی که شرایط بالا رو دارند
    due_soldier_ids = [entry['normal_letter__soldier'] for entry in latest_letters]

    # پیدا کردن آخرین نامه‌های آن سربازها
    due_letters = NormalLetterMentalHealthAssessmentAndEvaluation.objects.filter(
        normal_letter__soldier__in=due_soldier_ids
    ).order_by('normal_letter__soldier', '-created_at').distinct('normal_letter__soldier')

    context = {
        'due_letters': due_letters,
    }
    return render(request, 'soldires_apps/due_mental_health_letters.html', context)


def soldiers_by_entry_date(request):
    soldiers = []
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        try:
            # تبدیل تاریخ‌های شمسی به میلادی
            from_parts = list(map(int, from_date.split('/')))
            to_parts = list(map(int, to_date.split('/')))
            from_gregorian = jdatetime.date(*from_parts).togregorian()
            to_gregorian = jdatetime.date(*to_parts).togregorian()

            soldiers = Soldier.objects.filter(
                service_entry_date__range=(from_gregorian, to_gregorian)
            ).order_by('service_entry_date')

        except Exception as e:
            print("خطا در تبدیل تاریخ:", e)

    return render(request, 'soldires_apps/soldiers_by_entry_date.html', {
        'soldiers': soldiers,
        'from_date': from_date,
        'to_date': to_date
    })


def incomplete_soldiers_list(request):
    from .models import Soldier
    soldiers = Soldier.objects.all()
    return render(request, 'soldires_apps/incomplete_soldiers_list.html', {'soldiers': soldiers})
