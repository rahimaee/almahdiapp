from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import ParentUnit, SubUnit
from .forms import ParentUnitForm, SubUnitForm


# لیست واحدهای اصلی
def parent_unit_list(request):
    parent_units = ParentUnit.objects.all()
    return render(request, 'units_apps/parent_unit_list.html', {'parent_units': parent_units})


# ایجاد یا ویرایش واحد اصلی
def parent_unit_form(request, pk=None):
    if pk:
        parent_unit = get_object_or_404(ParentUnit, pk=pk)
    else:
        parent_unit = None

    if request.method == 'POST':
        form = ParentUnitForm(request.POST, instance=parent_unit)
        if form.is_valid():
            form.save()
            return redirect('parent_unit_list')
    else:
        form = ParentUnitForm(instance=parent_unit)

    return render(request, 'units_apps/parent_unit_form.html', {'form': form})


# حذف واحد اصلی
def parent_unit_delete(request, pk):
    parent_unit = get_object_or_404(ParentUnit, pk=pk)
    if request.method == 'POST':
        parent_unit.delete()
        return redirect('parent_unit_list')

    return render(request, 'units_apps/parent_unit_delete.html', {'parent_unit': parent_unit})



# لیست زیرواحدها
def sub_unit_list(request):
    sub_units = SubUnit.objects.all()
    return render(request, 'units_apps/sub_unit_list.html', {'sub_units': sub_units})

# ایجاد یا ویرایش زیرواحد
def sub_unit_form(request, pk=None):
    if pk:
        sub_unit = get_object_or_404(SubUnit, pk=pk)
    else:
        sub_unit = None

    if request.method == 'POST':
        form = SubUnitForm(request.POST, instance=sub_unit)
        if form.is_valid():
            form.save()
            return redirect('sub_unit_list')
    else:
        form = SubUnitForm(instance=sub_unit)

    return render(request, 'units_apps/sub_unit_form.html', {'form': form})

# حذف زیرواحد
def sub_unit_delete(request, pk):
    sub_unit = get_object_or_404(SubUnit, pk=pk)
    if request.method == 'POST':
        sub_unit.delete()
        return redirect('sub_unit_list')
    return render(request, 'units_apps/sub_unit_delete.html', {'sub_unit': sub_unit})