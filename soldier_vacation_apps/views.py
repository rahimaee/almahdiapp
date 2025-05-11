from django.shortcuts import render, get_object_or_404, redirect
from .models import LeaveBalance
from soldires_apps.models import Soldier
from .forms import LeaveBalanceForm


# Create your views here.

def manage_soldier_vacation(request, soldier_id):
    soldier = get_object_or_404(Soldier, id=soldier_id)
    vacation, created = LeaveBalance.objects.get_or_create(soldier=soldier)

    if request.method == "POST":
        form = LeaveBalanceForm(request.POST, instance=vacation)  # استفاده از فرم
        if form.is_valid():
            form.save()
            return redirect('soldier_list')
    else:
        form = LeaveBalanceForm(instance=vacation)

    return render(request, 'soldier_vacation_apps/soldier_vacation_edit.html', {'form': form, 'soldier': soldier})
