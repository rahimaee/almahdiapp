from django.shortcuts import render, get_object_or_404, redirect
from soldires_apps.models import Soldier
from .models import SoldierDocuments
from .forms import SoldierDocumentsForm
from django.db import transaction, IntegrityError


def manage_soldier_documents(request, soldier_id):
    while True:
        try:
            with transaction.atomic():
                soldier = get_object_or_404(Soldier, id=soldier_id)
                document, created = SoldierDocuments.objects.get_or_create(soldier=soldier)

                if request.method == "POST":
                    form = SoldierDocumentsForm(request.POST, instance=document)
                    if form.is_valid():
                        print("IS VALID")
                        form.save()
                        # ✅ بعد از ذخیره دوباره برگرد به همین صفحه
                        return redirect(request.path)
                else:
                    form = SoldierDocumentsForm(instance=document)
                
                completed_docs = [f for f in form if f.value()]
                incomplete_docs = [f for f in form if not f.value()]

                ctx =  {
                    'soldier': soldier,
                    'form': form,
                    'completed_docs': len(completed_docs),
                    'incomplete_docs': len(incomplete_docs)
                }
                template=  'soldier_documents_apps/soldier_documents_form.html'
                return render(request, template,ctx)
        except IntegrityError:
            continue
