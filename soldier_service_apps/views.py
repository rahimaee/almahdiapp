from django.views.generic.edit import UpdateView
from .models import SoldierService
from django.urls import reverse_lazy
from .forms import SoldierServiceForm


class SoldierServiceUpdateView(UpdateView):
    model = SoldierService
    form_class = SoldierServiceForm
    template_name = 'soldier_service_apps/soldier_service_edit.html'
    success_url = reverse_lazy('soldier_list')  # صفحه‌ای که بعد از ویرایش نشان داده می‌شود

    def get_object(self, queryset=None):
        soldier = self.kwargs.get('soldier_id')
        return SoldierService.objects.get(soldier_id=soldier)


