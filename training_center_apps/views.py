from django.shortcuts import render, get_object_or_404, redirect
from .models import TrainingCenter
from .forms import TrainingCenterForm


def training_center_list(request):
    centers = TrainingCenter.objects.all()
    return render(request, 'training_center_apps/training_center_list.html', {'centers': centers})


def training_center_create(request):
    if request.method == 'POST':
        form = TrainingCenterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training_center_list')
    else:
        form = TrainingCenterForm()
    return render(request, 'training_center_apps/training_center_form.html', {'form': form})


def training_center_edit(request, pk):
    center = get_object_or_404(TrainingCenter, pk=pk)
    if request.method == 'POST':
        form = TrainingCenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            return redirect('training_center_list')
    else:
        form = TrainingCenterForm(instance=center)
    return render(request, 'training_center_apps/training_center_form.html', {'form': form})


def training_center_delete(request, pk):
    center = get_object_or_404(TrainingCenter, pk=pk)
    if request.method == 'POST':
        center.delete()
        return redirect('training_center_list')
    return render(request, 'training_center_apps/training_center_confirm_delete.html', {'center': center})
