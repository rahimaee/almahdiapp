from django.views.generic import ListView

from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import ClearanceLetter
from .forms import ClearanceLetterForm
from django.db.models import Q

class ClearanceLetterCreateView(CreateView):
    model = ClearanceLetter
    form_class = ClearanceLetterForm
    template_name = 'soldire_letter_apps/ClearanceLetter_create.html'
    success_url = reverse_lazy('ClearanceLetterListView')  # یا هر URL دلخواه


class ClearanceLetterListView(ListView):
    model = ClearanceLetter
    template_name = 'soldire_letter_apps/ClearanceLetter_list.html'
    context_object_name = 'letters'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset().select_related('soldier')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(letter_number__icontains=query) |
                Q(soldier__first_name__icontains=query) |
                Q(soldier__last_name__icontains=query) |
                Q(soldier__national_code__icontains=query)
            )
        return queryset.order_by('-issue_date')

