from django.shortcuts import render, redirect, get_object_or_404
from accounts_apps.decorators import feature_required
from soldires_apps.models import Soldier
from .models import NaserinGroup
from .forms import NaserinGroupForm
from accounts_apps.models import MyUser
from django.db import transaction, IntegrityError


@feature_required('ایجاد گروه ناصرین')
def naserin_create(request):
    if request.method == 'POST':
        form = NaserinGroupForm(request.POST)
        while True:
            try:
                with transaction.atomic():
                    if form.is_valid():
                        form.save()
                        return redirect('naserin_list')
                break
            except IntegrityError:
                continue
    else:
        form = NaserinGroupForm()
    return render(request, 'soldire_naserin_apps/create.html', {'form': form})


@feature_required('ویرایش گروه ناصرین')
def naserin_edit(request, pk):
    group = get_object_or_404(NaserinGroup, pk=pk)
    if request.method == 'POST':
        form = NaserinGroupForm(request.POST, instance=group)
        while True:
            try:
                with transaction.atomic():
                    if form.is_valid():
                        form.save()
                        return redirect('naserin_list')
                break
            except IntegrityError:
                continue
    else:
        form = NaserinGroupForm(instance=group)
    return render(request, 'soldire_naserin_apps/edit.html', {'form': form, 'group': group})


@feature_required('لیست گروه‌های ناصرین')
def naserin_list(request):
    while True:
        try:
            with transaction.atomic():
                groups = NaserinGroup.objects.all()
                return render(request, 'soldire_naserin_apps/list.html', {'groups': groups})
        except IntegrityError:
            continue


# word here i mohammad
@feature_required('جدول افراد و گروه های ناصرین')
def soldire_naserin_list(request):
    while True:
        try:
            with transaction.atomic():
                groups = NaserinGroup.objects.all()
                if request.user.is_authenticated:
                    if request.user.is_superuser:
                        soldires = Soldier.objects.filter(is_checked_out=False).all()
                    else:
                        soldires = Soldier.objects.filter(is_checked_out=False, naserin_group__manager_id=request.user.id).all()
                return render(request, 'soldire_naserin_apps/soldire_naserin_list.html', {'soldires': soldires})
        except IntegrityError:
            continue


@feature_required('ویرایش گروه ناصرین سربازان')
def edit_soldier_naserin(request, soldier_id):
    soldier = get_object_or_404(Soldier, id=soldier_id)
    naserin_groups = NaserinGroup.objects.all()

    if request.method == 'POST':
        group_id = request.POST.get('naserin_group')
        while True:
            try:
                with transaction.atomic():
                    soldier.naserin_group_id = group_id
                    soldier.save()
                    return redirect('soldier_list')
            except IntegrityError:
                continue

    return render(request, 'soldire_naserin_apps/form_single_edit.html', {
        'soldier': soldier,
        'naserin_groups': naserin_groups
    })


@feature_required('تخصیص گروه ناصرین به سربازان فاقد گروهی')
# اختصاص گروه ناصرین به چند سرباز
def bulk_edit_naserin(request):
    soldiers = Soldier.objects.all()
    naserin_groups = NaserinGroup.objects.all()

    if request.method == 'POST':
        selected_soldiers = request.POST.getlist('soldier_ids')
        group_id = request.POST.get('naserin_group')
        while True:
            try:
                with transaction.atomic():
                    Soldier.objects.filter(id__in=selected_soldiers).update(naserin_group_id=group_id)
                    return redirect('soldier_list')
            except IntegrityError:
                continue

    return render(request, 'soldire_naserin_apps/form_bulk_edit.html', {
        'soldiers': soldiers,
        'naserin_groups': naserin_groups
    })
