from django.shortcuts import render, redirect, get_object_or_404
from soldires_apps.models import Soldier
from .models import ReligiousPeriod
from .forms import ReligiousPeriodForm, SoldierIdeologicalForm, ExcelUploadForm
import pandas as pd


def create_religious_period(request):
    if request.method == 'POST':
        form = ReligiousPeriodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('religious_period_list')
    else:
        form = ReligiousPeriodForm()
    return render(request, 'soldire_religious_period_apps/religious_period_form.html', {'form': form})


def update_religious_period(request, pk):
    period = get_object_or_404(ReligiousPeriod, pk=pk)
    if request.method == 'POST':
        form = ReligiousPeriodForm(request.POST, instance=period)
        if form.is_valid():
            form.save()
            return redirect('religious_period_list')
    else:
        form = ReligiousPeriodForm(instance=period)
    return render(request, 'soldire_religious_period_apps/religious_period_form.html', {'form': form})


def religious_period_list(request):
    periods = ReligiousPeriod.objects.all()
    return render(request, 'soldire_religious_period_apps/religious_period_list.html', {'periods': periods})


def soldiers_without_ideological_training(request):
    # دریافت سربازانی که دوره عقیدتی ندارند
    soldiers = Soldier.objects.filter(ideological_training_period__isnull=True)
    return render(request, 'soldire_religious_period_apps/soldiers_without_training.html', {'soldiers': soldiers})


def soldiers_with_religious_period(request):
    soldiers = Soldier.objects.filter(ideological_training_period__isnull=False)
    return render(request, 'soldire_religious_period_apps/soldiers_with_training.html', {'soldiers': soldiers})


def edit_ideological_period(request, soldier_id):
    soldier = get_object_or_404(Soldier, id=soldier_id)
    if request.method == 'POST':
        form = SoldierIdeologicalForm(request.POST, instance=soldier)
        if form.is_valid():
            form.save()
            return redirect('soldier_detail', pk=soldier.id)  # یا هر آدرس دیگری
    else:
        form = SoldierIdeologicalForm(instance=soldier)
    return render(request, 'soldire_religious_period_apps/edit_ideological.html', {'form': form, 'soldier': soldier})


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
                    national_code = str(row.get('کدملی')).strip()
                    period_id = row.get('شماره دوره')

                    if not national_code or pd.isna(period_id):
                        errors.append(f"❌ ردیف {index + 2}: اطلاعات ناقص")
                        continue

                    try:
                        soldier = Soldier.objects.get(national_code=national_code)
                        period = ReligiousPeriod.objects.get(id=int(period_id))
                        soldier.ideological_training_period = period
                        soldier.save()
                        success_count += 1
                    except Soldier.DoesNotExist:
                        errors.append(f"❌ ردیف {index + 2}: سرباز با کدملی {national_code} یافت نشد.")
                    except ReligiousPeriod.DoesNotExist:
                        errors.append(f"❌ ردیف {index + 2}: دوره با شناسه {period_id} یافت نشد.")
                    except Exception as e:
                        errors.append(f"⚠️ ردیف {index + 2}: خطا - {str(e)}")

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
