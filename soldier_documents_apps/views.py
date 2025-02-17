from django.shortcuts import render, get_object_or_404, redirect
from soldires_apps.models import Soldier
from .models import SoldierDocuments
from .forms import SoldierDocumentsForm


def manage_soldier_documents(request, soldier_id):
    soldier = get_object_or_404(Soldier, id=soldier_id)
    document, created = SoldierDocuments.objects.get_or_create(soldier=soldier)

    if request.method == "POST":
        form = SoldierDocumentsForm(request.POST, instance=document)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('soldier_list')  # تغییر دهید به مسیر مناسب
    else:

        form = SoldierDocumentsForm(instance=document)

    return render(request, 'soldier_documents_apps/soldier_documents_form.html', {'form': form, 'soldier': soldier})
