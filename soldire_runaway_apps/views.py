from django.core.paginator import Paginator
from django.shortcuts import render

from soldires_apps.models import Soldier
from .models import EscapeRecord
from django.shortcuts import get_object_or_404


def escaped_soldiers_view(request):
    query = request.GET.get('q', '')

    # فقط سربازهایی که هنوز بازنگشتن
    escaped_records = EscapeRecord.objects.filter(return_date__isnull=True).select_related('soldier')

    # فقط unique سربازها
    soldiers = {record.soldier for record in escaped_records}

    # اعمال جست‌وجو
    if query:
        soldiers = [s for s in soldiers if query in s.first_name or query in s.last_name or query in s.national_code]

    # صفحه‌بندی
    page = request.GET.get('page', 1)
    paginator = Paginator(list(soldiers), 100)  # 10 سرباز در هر صفحه
    page_obj = paginator.get_page(page)

    return render(request, 'soldire_runaway_apps/escaped_soldiers.html', {
        'page_obj': page_obj,
        'query': query
    })


def soldier_escape_details(request, soldier_id):
    soldier = get_object_or_404(Soldier, id=soldier_id)
    escapes = soldier.escapes.all()
    return render(request, 'soldire_runaway_apps/escape_details.html', {'soldier': soldier, 'escapes': escapes})
