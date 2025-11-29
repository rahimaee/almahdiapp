from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from soldires_apps.models import Soldier
from django.db.models import Count, Q  # اضافه کردن Count
import openpyxl
from openpyxl import Workbook
from django.http import HttpResponse
from openpyxl.styles import Alignment, Font, PatternFill
from datetime import datetime
from soldires_apps.utils import create_soldiers_excel
from django.utils import timezone
from datetime import timedelta
from soldire_letter_apps.models import ClearanceLetter   # اگر مسیرت متفاوت است، اصلاح کن
from django.db import models
from datetime import date, timedelta
from analystics.stats.base import *
from analystics.stats.items import *


@login_required
def home(request):
    soldires = Soldier.objects.filter(is_checked_out=False)
    allCount = Soldier.objects.all().count()
    soldiers_45_to_end = Soldier.date_to_ends(45).count() 
    # --- تاریخ‌ها برای فیلتر ---
    last_date = ClearanceLetter.objects.aggregate(last=models.Max('issue_date'))['last']
    today_date = last_date or timezone.now().date()
    last_week_start = today_date - timedelta(days=7)
    last_month_start = today_date - timedelta(days=30)
    # --- گرفتن نامه‌ها ---
    today_letters = ClearanceLetter.get_between_dates(start_date=today_date, end_date=today_date)
    last_week_letters = ClearanceLetter.get_between_dates(start_date=last_week_start, end_date=today_date)
    last_month_letters = ClearanceLetter.get_between_dates(start_date=last_month_start, end_date=today_date)
    no_accepted = ClearanceLetter.accepted_list(False)
    clearance_letters = {
        'today': today_letters,
        'last_week': last_week_letters,
        'last_month': last_month_letters,
        'no_accepted':no_accepted,
    }
    
    present = PresentSoldiers()
    counts_present = present.count()

    counts_fugitives = lambda: RunawaySoldiers().count()
    counts_all_soldiers = counts_fugitives() + counts_present

    counts_healthy_exemptb = lambda: ExemptBSoldiers(present).count()
    counts_healthy_safe   = lambda: HealthySoldiers(present).count()
    counts_healthy_exempt = lambda: ExemptSoldiers(present).count()

    counts_married = soldires.filter(marital_status='متاهل').count()
    counts_single  = soldires.filter(marital_status='مجرد').count()

    counts_absorption = lambda: AbsorptionSoldiers(present).count()

    stats = {
        'counts_all_soldiers':counts_all_soldiers,
        'counts_present':counts_present,
        'counts_fugitives':counts_fugitives,
        'counts_healthy_safe':counts_healthy_safe,
        'counts_healthy_exempt':counts_healthy_exempt,
        'counts_healthy_exemptb':counts_healthy_exemptb,
        'counts_married':counts_married,
        'counts_single':counts_single,
        'counts_absorption':counts_absorption,
        'with_card': soldires.filter(eligible_for_card_issuance=True).count(),
        'financial_debt': soldires.filter(file_shortage__isnull=False).exclude(file_shortage='').count(),
        'soldiers_45_to_end':soldiers_45_to_end,
    }

    today = date.today()
    r_today = Soldier.objects.filter(service_entry_date=today)
    r_day3 = Soldier.objects.filter(service_entry_date__gte=today - timedelta(days=3))
    r_day7 = Soldier.objects.filter(service_entry_date__gte=today - timedelta(days=7))
    r_day30 = Soldier.objects.filter(service_entry_date__gte=today - timedelta(days=30))
    registrations = {'r_today': r_today,'r_day3': r_day3,'r_day7': r_day7,'r_day30': r_day30 }


    #حاظر 
    present = PresentSoldiers()
    counts_present = present.count()
    counts_healthy_exemptb = ExemptBSoldiers(present).count()
    counts_healthy_safe   = HealthySoldiers(present).count()
    counts_healthy_exempt = ExemptSoldiers(present).count()
    counts_married = MarriedSoldiers(present).get_queryset().count()
    counts_single  = SingleSoldiers(present).get_queryset().count()
    counts_absorption = AbsorptionSoldiers(present).count()
    #فراری 
    fugitives = RunawaySoldiers()
    counts_fugitives = fugitives.count()
    counts_fugitives_healthy   = HealthySoldiers(fugitives).count()
    counts_fugitives_exempt    = ExemptSoldiers(fugitives).count()
    counts_fugitives_exemptb   = ExemptBSoldiers(fugitives).count()
    counts_fugitives_married = MarriedSoldiers(fugitives).count()
    counts_fugitives_single  = SingleSoldiers(fugitives).count()
    counts_fugitives_absorption = AbsorptionSoldiers(fugitives).count()

    # امار کل 
    counts_all_soldiers = counts_present + counts_fugitives
    counts_all_absorption = counts_absorption + counts_fugitives_absorption
    actions = [
        { "label": "دانلود اکسل", "icon": "📥", "base": "export_soldiers","disabled":True },
        { "label": "چاپ", "icon": "🖨️", "base": "export_soldiers" ,"disabled":True},
        { "label": "مشاهده", "icon": "👁️", "base": "export_soldiers" ,"disabled":True},
    ]
    
    education_counts = EducationGroup(present).get_grouped_counts()
    rank_counts = RankGroup(present).get_grouped_counts()
    
    analytics = [
        {
            'col':4,
            "label": "سربازان حاضر",
            "gradient": "gradient-green",
            "count": counts_present,
            "query": "present",
            "actions": actions,
            "items": [
                { "label": "سالم", "count": counts_healthy_safe, "query": "healthy" },
                { "label": "معاف از رزم", "count": counts_healthy_exempt, "query": "exempt" },
                { "label": "گروه ب", "count": counts_healthy_exemptb, "query": "exemptb" },
                { "label": "متأهل", "count": counts_married, "query": "married" },
                { "label": "مجرد", "count": counts_single, "query": "single" },
                { "label": "جذبی", "count": counts_absorption, "query": "absorption" },
            ]
        },
        {
            'col':4,
            "label": "سربازان فراری",
            "gradient": "gradient-red",
            "count": counts_fugitives,
            "query": "fugitives",
            "actions": actions,
            "items": [
                { "label": "سالم", "count": counts_fugitives_healthy, "query": "healthy" },
                { "label": "معاف از رزم", "count": counts_fugitives_exempt, "query": "exempt" },
                { "label": "گروه ب", "count": counts_fugitives_exemptb, "query": "exemptb" },
                { "label": "متأهل", "count": counts_fugitives_married, "query": "married" },
                { "label": "مجرد", "count": counts_fugitives_single, "query": "single" },
                { "label": "جذبی", "count": counts_fugitives_absorption, "query": "single" },
            ]
        },
        {
            'col':4,
            "label": "آمار کل سربازان",
            "gradient": "gradient-blue",
            "count": counts_all_soldiers,
            "query": "category=all",
            "actions": actions,
            "items": [
                { "label": "حاضر", "count": counts_present, "query": "present" },
                { "label": "فراری", "count": counts_fugitives, "query": "fugitives" },
                { "label": "جذبی", "count": counts_all_absorption, "query": "category=financial_debt" },
                { "label": "45 روز تا پایان", "count": Soldier.date_to_ends(45).count(), "query": "remainingFilter=remaining45" },
                { "label": "30 روز تا پایان", "count": Soldier.date_to_ends(30).count(), "query": "remainingFilter=remaining30" },
                { "label": "15 روز تا پایان", "count": Soldier.date_to_ends(15).count(), "query": "remainingFilter=remaining15" },
            ]
        },
        {
            'col':6,
            "label": "تحصیلات و مدرک ",
            "gradient": "gradient-gray",
            "query": "all",
            "actions": actions,
            "items": [
                { "label": degree, "count": count, "query": f"degree_{i}" }
                for i, (degree, count) in enumerate(education_counts.items(), start=1)
            ]
        },
        {
            'col':6,
            "label": "درجات و ترفیعات",
            "gradient": "gradient-purple",
            "query": "all",
            "actions": actions,
            'itemsCol':3,
            "items": [
                { "label": rank, "count": count, "query": f"rank_{i}" }
                for i, (rank, count) in enumerate(rank_counts.items(), start=1)
            ]
        },

    ]


    context = {
        'analytics':analytics,
        'stats': stats,
        'soldires': soldires,
        'clearance_letters':clearance_letters,
        'registrations':registrations,
    }

    return render(request, 'home_apps/home.html', context)


def header_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_Header.html')


def header_references_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_HeaderReferences.html')


def navbar_partial_view(request, *args, **kwargs):
    user = request.user.is_staff == True
    return render(request, 'shared/_Navbar.html')


def footer_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_Footer.html')


def footer_references_partial_view(request, *args, **kwargs):
    return render(request, 'shared/_FooterReferences.html')


def manages_app(request):
    return render(request, 'manage_apps/index.html')



@login_required
def export_soldiers_excel(request):
    category = request.GET.get('category', 'all')

    # فیلتر بر اساس category
    soldiers = Soldier.objects.all()
    if category == 'active':
        soldiers = soldiers.filter(is_checked_out=False)
    elif category == 'fugitives':
        soldiers = soldiers.filter(is_fugitive=True)
    elif category == 'administrative':
        soldiers = soldiers.filter(status='توجیحی')
    elif category == 'shifted':
        soldiers = soldiers.filter(status='حین خدمت')
    elif category == 'posted':
        soldiers = soldiers.filter(status='پایان خدمت')
    elif category == 'transferred':
        soldiers = soldiers.filter(status='انتقالی')
    elif category == 'married':
        soldiers = soldiers.filter(marital_status='متاهل')
    elif category == 'single':
        soldiers = soldiers.filter(marital_status='مجرد')
    elif category == 'with_card':
        soldiers = soldiers.filter(eligible_for_card_issuance=True)
    elif category == 'health_salam':
        soldiers = soldiers.filter(health_status='سالم')
    elif category == 'health_exempt':
        soldiers = soldiers.filter(health_status='معاف از رزم')
    elif category == 'health_group_b':
        soldiers = soldiers.filter(health_status='گروه ب')
    elif category == 'health_exempt_b':
        soldiers = soldiers.filter(health_status='معاف+گروه ب')

    now_str = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"soldiers_{category}_{now_str}"
    wb = create_soldiers_excel(soldiers)

    response = HttpResponse(
        content=openpyxl.writer.excel.save_virtual_workbook(wb),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
    return response