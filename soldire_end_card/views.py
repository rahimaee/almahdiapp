from soldires_apps.models import Settlement
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import CardSeries, CardSend
from .forms import CardSeriesForm, CardSendReviewForm, CardSendForm


# Create your views here.
def soldiers_ready_for_card(request):
    # لیست سربازان آماده برای ارسال کارت (بدون بدهی و تسویه کامل)
    soldiers_ready_for_card = Settlement.objects.filter(current_debt_rial=0, status='cleared')

    return render(request, 'soldire_end_card/settlement_list_ready_for_card.html', {
        'soldiers_ready_for_card': soldiers_ready_for_card,
    })


def card_series_list(request):
    series = CardSeries.objects.all()
    return render(request, 'soldire_end_card/card_series_list.html', {'series': series})


def card_series_create(request):
    form = CardSeriesForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('card_series_list')
    return render(request, 'soldire_end_card/card_series_form.html', {'form': form, 'title': 'ایجاد سری کارت'})


def card_series_edit(request, pk):
    obj = get_object_or_404(CardSeries, pk=pk)
    form = CardSeriesForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('card_series_list')
    return render(request, 'soldire_end_card/card_series_form.html', {'form': form, 'title': 'ویرایش سری کارت'})


def resend_unissued_cards(request, series_id):
    old_series = CardSeries.objects.get(id=series_id)
    new_series = CardSeries.objects.create(title="سری جدید", send_date=timezone.now(), status='preparing')

    unissued_cards = CardSend.objects.filter(series=old_series, is_issued=False)
    for old_card in unissued_cards:
        CardSend.objects.create(soldier=old_card.soldier, series=new_series)

    return redirect("card_series_list")


def review_card_send(request, pk):
    card = get_object_or_404(CardSend, pk=pk)
    if request.method == "POST":
        form = CardSendReviewForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect("card_send_list", series_id=card.series.id)
    else:
        form = CardSendReviewForm(instance=card)
    return render(request, "soldire_end_card/review_card_send.html", {"form": form, "card": card})


def card_send_list_n(request):
    cards = CardSend.objects.select_related('series', 'soldier').all().order_by('-created_at')
    return render(request, 'soldire_end_card/card_send_list_n.html', {'cards': cards})


def card_send_list_series(request, series_id):
    cards = CardSend.objects.filter(series_id=series_id).all().order_by('-created_at')
    return render(request, 'soldire_end_card/card_send_list_n.html', {'cards': cards})


def card_send_create(request):
    if request.method == 'POST':
        form = CardSendForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('card_send_list')  # صفحه‌ای که لیست کارت‌ها را نمایش می‌دهد
    else:
        form = CardSendForm()
    return render(request, 'soldire_end_card/card_send_form.html', {'form': form, 'title': 'ثبت کارت جدید'})


def card_send_update(request, pk):
    card_send = get_object_or_404(CardSend, pk=pk)
    if request.method == 'POST':
        form = CardSendForm(request.POST, instance=card_send)
        if form.is_valid():
            form.save()
            return redirect('card_send_list')
    else:
        form = CardSendForm(instance=card_send)
    return render(request, 'soldire_end_card/card_send_form.html', {'form': form, 'title': 'ویرایش کارت'})


def card_send_create_for_soldier(request, soldier_id):
    from soldires_apps.models import Soldier
    soldier = get_object_or_404(Soldier, pk=soldier_id)

    if request.method == 'POST':
        form = CardSendForm(request.POST, soldier_fixed=True)
        if form.is_valid():
            card = form.save(commit=False)
            card.soldier = soldier
            card.save()
            return redirect('card_send_list')
    else:
        form = CardSendForm(initial={'soldier': soldier.id}, soldier_fixed=True)

    return render(request, 'soldire_end_card/card_send_form.html', {
        'form': form,
        'title': f'اختصاص کارت به سرباز: {soldier}'
    })
