from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .forms import SoldierServiceForm
from .models import SoldierService,get_service
from soldires_apps.models import Soldier
from django.db import transaction, IntegrityError
from django.urls import reverse
   
class SoldierServiceUpdateView(View):
    template_name = 'soldier_service_apps/soldier_service_edit.html'
    
    
    
    def get(self, request, soldier_id):
        soldier = get_object_or_404(Soldier, id=soldier_id)
        obj = get_service(soldier)
        form = SoldierServiceForm(instance=obj)
        return render(request, self.template_name, {'form': form, 'soldier': soldier})

    def post(self, request, soldier_id):
        soldier = get_object_or_404(Soldier, id=soldier_id)
        obj = get_service(soldier)
        form = SoldierServiceForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('soldier_service_edit', args=[soldier.id]))
        return render(request, self.template_name, {'form': form, 'soldier': soldier})
