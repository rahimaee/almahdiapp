from django.shortcuts import render, redirect, get_object_or_404

from soldires_apps.models import Soldier
from .models import NaserinGroup
from .forms import NaserinGroupForm


def naserin_create(request):
    if request.method == 'POST':
        form = NaserinGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('naserin_list')  # تغییر بده به مسیر لیست یا صفحه مورد نظر
    else:
        form = NaserinGroupForm()
    return render(request, 'soldire_naserin_apps/create.html', {'form': form})


def naserin_edit(request, pk):
    group = get_object_or_404(NaserinGroup, pk=pk)
    if request.method == 'POST':
        form = NaserinGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('naserin_list')
    else:
        form = NaserinGroupForm(instance=group)
    return render(request, 'soldire_naserin_apps/edit.html', {'form': form, 'group': group})


def naserin_list(request):
    groups = NaserinGroup.objects.all()
    return render(request, 'soldire_naserin_apps/list.html', {'groups': groups})


def soldire_naserin_list(request):
    groups = NaserinGroup.objects.all()
    return render(request, 'soldire_naserin_apps/soldire_naserin_list.html', {'groups': groups})


def edit_soldier_naserin(request, soldier_id):
    soldier = get_object_or_404(Soldier, id=soldier_id)
    naserin_groups = NaserinGroup.objects.all()

    if request.method == 'POST':
        group_id = request.POST.get('naserin_group')
        soldier.naserin_group_id = group_id
        soldier.save()
        return redirect('soldier_list')  # می‌تونی ریدایرکت کنی به هر صفحه‌ای

    return render(request, 'soldire_naserin_apps/form_single_edit.html', {
        'soldier': soldier,
        'naserin_groups': naserin_groups
    })


# اختصاص گروه ناصرین به چند سرباز
def bulk_edit_naserin(request):
    soldiers = Soldier.objects.all()
    naserin_groups = NaserinGroup.objects.all()

    if request.method == 'POST':
        selected_soldiers = request.POST.getlist('soldier_ids')
        group_id = request.POST.get('naserin_group')
        Soldier.objects.filter(id__in=selected_soldiers).update(naserin_group_id=group_id)
        return redirect('soldier_list')

    return render(request, 'soldire_naserin_apps/form_bulk_edit.html', {
        'soldiers': soldiers,
        'naserin_groups': naserin_groups
    })
