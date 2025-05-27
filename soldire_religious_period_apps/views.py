from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction, IntegrityError
from accounts_apps.decorators import feature_required
from soldires_apps.models import Soldier
from .models import ReligiousPeriod
from .forms import ReligiousPeriodForm, SoldierIdeologicalForm, ExcelUploadForm
import pandas as pd

@feature_required('ایجاد دوره عقیدتی')
def create_religious_period(request):
    while True:
        try:
            with transaction.atomic():
                if request.method == 'POST':
                    form = ReligiousPeriodForm(request.POST)
                    if form.is_valid():
                        form.save()
                        return redirect('religious_period_list')
                else:
                    form = ReligiousPeriodForm()
                return render(request, 'soldire_religious_period_apps/religious_period_form.html', {'form': form})
        except IntegrityError:
            continue

@feature_required('ویرایش دوره عقیدتی')
def update_religious_period(request, pk):
    while True:
        try:
            with transaction.atomic():
                period = get_object_or_404(ReligiousPeriod, pk=pk)
                if request.method == 'POST':
                    form = ReligiousPeriodForm(request.POST, instance=period)
                    if form.is_valid():
                        form.save()
                        return redirect('religious_period_list')
                else:
                    form = ReligiousPeriodForm(instance=period)
                return render(request, 'soldire_religious_period_apps/religious_period_form.html', {'form': form})
        except IntegrityError:
            continue

@feature_required('لیست عقیدتی')
def religious_period_list(request):
    while True:
        try:
            with transaction.atomic():
                periods = ReligiousPeriod.objects.all()
                return render(request, 'soldire_religious_period_apps/religious_period_list.html', {'periods': periods})
        except IntegrityError:
            continue

@feature_required('لیست سربازانی که دوره عقیدتی ندارند')
def soldiers_without_ideological_training(request):
    while True:
        try:
            with transaction.atomic():
                soldiers = Soldier.objects.filter(ideological_training_period__isnull=True, is_checked_out=False)
                return render(request, 'soldire_religious_period_apps/soldiers_without_training.html', {'soldiers': soldiers})
        except IntegrityError:
            continue

@feature_required('لیست سربازان و دوره عقیدتی')
def soldiers_with_religious_period(request):
    while True:
        try:
            with transaction.atomic():
                soldiers = Soldier.objects.filter(ideological_training_period__isnull=False, is_checked_out=False)
                return render(request, 'soldire_religious_period_apps/soldiers_with_training.html', {'soldiers': soldiers})
        except IntegrityError:
            continue

@feature_required('تخصیص دوره عقیدتی به فرد')
def edit_ideological_period(request, soldier_id):
    while True:
        try:
            with transaction.atomic():
                soldier = get_object_or_404(Soldier, id=soldier_id)
                if request.method == 'POST':
                    form = SoldierIdeologicalForm(request.POST, instance=soldier)
                    if form.is_valid():
                        form.save()
                        return redirect('soldier_detail', pk=soldier.id)
                else:
                    form = SoldierIdeologicalForm(instance=soldier)
                return render(request, 'soldire_religious_period_apps/edit_ideological.html', {'form': form, 'soldier': soldier})
        except IntegrityError:
            continue

@feature_required('آپلود فایل اکسل دوره عقیدتی')
def upload_excel_view(request):
    errors = []
    success_count = 0

    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']

            try:
                df = pd.read_excel(file)

                for index, row in df.iterrows():
                    while True:
                        try:
                            with transaction.atomic():
                                national_code = str(row.get('کدملی')).strip()
                                period_id = row.get('شماره دوره')

                                if not national_code or pd.isna(period_id):
                                    errors.append(f"❌ ردیف {index + 2}: اطلاعات ناقص")
                                    break

                                soldier = Soldier.objects.get(national_code=national_code)
                                period = ReligiousPeriod.objects.get(id=int(period_id))
                                soldier.ideological_training_period = period
                                soldier.save()
                                success_count += 1
                                break
                        except IntegrityError:
                            continue
                        except Soldier.DoesNotExist:
                            errors.append(f"❌ ردیف {index + 2}: سرباز با کدملی {national_code} یافت نشد.")
                            break
                        except ReligiousPeriod.DoesNotExist:
                            errors.append(f"❌ ردیف {index + 2}: دوره با شناسه {period_id} یافت نشد.")
                            break
                        except Exception as e:
                            errors.append(f"⚠️ ردیف {index + 2}: خطا - {str(e)}")
                            break

            except Exception as e:
                errors.append(f"⚠️ خطا در خواندن فایل: {str(e)}")

            return render(request, 'soldire_religious_period_apps/upload_result.html', {
                'form': ExcelUploadForm(),
                'errors': errors,
                'success_count': success_count,
                'total': len(df),
            })
    else:
        form = ExcelUploadForm()

    return render(request, 'soldire_religious_period_apps/upload_form.html', {'form': form})
