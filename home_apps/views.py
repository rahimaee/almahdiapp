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


    #حاضر 
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
        { "label": "دانلود اکسل", "icon": "📥", "base": "export_soldiers","disabled":False,'show':request.user.is_staff },
        { "label": "چاپ", "icon": "🖨️", "base": "export_soldiers" ,"disabled":True,'show':request.user.is_staff},
        { "label": "مشاهده", "icon": "👁️", "base": "soldier_list" ,"disabled":False,'show':True},
    ]
    
    education_counts = EducationGroup(present).get_grouped_counts()
    rank_counts = RankGroup(present).get_grouped_counts()

    entry_exit_acions = actions = [
        { "label": "دانلود اکسل", "icon": "📥", "base": "export_soldiers","disabled":False,'show':request.user.is_staff },
        { "label": "چاپ", "icon": "🖨️", "base": "export_soldiers" ,"disabled":True,'show':request.user.is_staff},
        { "label": "مشاهده", "icon": "👁️", "base": "soldier_list" ,"disabled":False,'show':True},
    ]

    analytics = [
        {
            'col':4,
            "label": "آمار کل سربازان",
            "gradient": "gradient-blue",
            "count": counts_all_soldiers,
            "actions": actions,
            "items": [
                { "label": "حاضر", "count": counts_present, "query": "defaultFilter=present" },
                { "label": "فراری", "count": counts_fugitives, "query": "defaultFilter=absent" },
                { "label": "جذبی", "count": counts_all_absorption, "query": "absorption=True" },
                { "label": "45 روز تا پایان", "count": Soldier.date_to_ends(45).count(), "query": "defaultFilter=present&remainingFilter=remaining45" },
                { "label": "30 روز تا پایان", "count": Soldier.date_to_ends(30).count(), "query": "defaultFilter=present&remainingFilter=remaining30" },
                { "label": "15 روز تا پایان", "count": Soldier.date_to_ends(15).count(), "query": "defaultFilter=present&remainingFilter=remaining15" },
            ]
        },
        {
            'col':4,
            "label": "حاضر به خدمت",
            "gradient": "gradient-green",
            "count": counts_present,
            "query": "defaultFilter=present",
            "actions": actions,
            "items": [
                { "label": "سالم", "count": counts_healthy_safe,            "query": "health_status=سالم" },
                { "label": "معاف از رزم", "count": counts_healthy_exempt,   "query": "health_status=معاف از رزم" },
                { "label": "گروه ب", "count": counts_healthy_exemptb,       "query": "health_status=معاف+گروه ب" },
                { "label": "متأهل", "count": counts_married,                "query": "marital_status=متاهل" },
                { "label": "مجرد", "count": counts_single,                  "query": "marital_status=مجرد" },
                { "label": "جذبی", "count": counts_absorption,              "query": "absorption=True" },
            ]
        },
        {
            'col':4,
            "label": "فرار از خدمت",
            "gradient": "gradient-red",
            "count": counts_fugitives,
            "query": "defaultFilter=absent",
            "actions": actions,
            "items": [
                { "label": "سالم", "count": counts_fugitives_healthy,           "query": "health_status=سالم" },
                { "label": "معاف از رزم", "count": counts_fugitives_exempt,     "query": "health_status=معاف از رزم" },
                { "label": "گروه ب", "count": counts_fugitives_exemptb,        "query": "health_status=معاف+گروه ب"  },
                { "label": "متأهل", "count": counts_fugitives_married,          "query": "marital_status=متاهل" },
                { "label": "مجرد", "count": counts_fugitives_single,            "query": "marital_status=مجرد" },
                { "label": "جذبی", "count": counts_fugitives_absorption,        "query": "absorption=True" },
            ]
        },
        
        {
            'col':5,
            "label": "تحصیلات و مدرک ",
            "gradient": "gradient-gray",
            "query": "present",
            "actions": actions,
            "items": [
                { "label": degree, "count": count, "query": f"degree={degree}" }
                for i, (degree, count) in enumerate(education_counts.items(), start=1)
            ]
        },
        {
            'col':7,
            "label": "درجات و ترفیعات",
            "gradient": "gradient-purple",
            "query": "present",
            "actions": actions,
            'itemsCol':3,
            "items": [
                { "label": rank, "count": count, "query": f"rank={rank}" }
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

from io import BytesIO

@login_required
def export_soldiers_excel(request):
    parent = request.GET.get('parent', 'all')
    item = request.GET.get('item', '')

    print(parent,item)
    # ===============================
    # تعیین والد (present / fugitives / all)
    # ===============================
    if parent == "present":
        soldiers = PresentSoldiers().get_queryset()
    elif parent == "fugitives":
        soldiers = RunawaySoldiers().get_queryset()
    else:
        soldiers = AllSoldiers().get_queryset()

    # ===============================
    # فیلترهای مشابه صفحه home
    # ===============================

    if item == "healthy":
        soldiers = HealthySoldiers(soldiers).get_queryset()
    elif item == "exempt":
        soldiers = ExemptSoldiers(soldiers).get_queryset()
    elif item == "exemptb":
        soldiers = ExemptBSoldiers(soldiers).get_queryset()
    elif item == "married":
        soldiers = MarriedSoldiers(soldiers).get_queryset()
    elif item == "single":
        soldiers = SingleSoldiers(soldiers).get_queryset()
    elif item == "absorption":
        soldiers = AbsorptionSoldiers(soldiers).get_queryset()

    # ============ مانده خدمت ============
    elif item == "remaining45":
        soldiers = Soldier.date_to_ends(45).filter(id__in=soldiers)
    elif item == "remaining30":
        soldiers = Soldier.date_to_ends(30).filter(id__in=soldiers)
    elif item == "remaining15":
        soldiers = Soldier.date_to_ends(15).filter(id__in=soldiers)

    # ============ گروه تحصیلی ============
    elif item.startswith("degree_"):
        index = int(item.split("_")[1])
        edu_map = list(EducationGroup(soldiers).get_grouped_counts().keys())
        if index <= len(edu_map):
            selected = edu_map[index - 1]
            soldiers = soldiers.filter(degree=selected)

    # ============ گروه درجه ============
    elif item.startswith("rank_"):
        index = int(item.split("_")[1])
        rank_map = list(RankGroup(soldiers).get_grouped_counts().keys())
        if index <= len(rank_map):
            selected = rank_map[index - 1]
            soldiers = soldiers.filter(rank=selected)

    # ============ ساخت فایل اکسل ============
    wb = create_soldiers_excel(soldiers)

    # ذخیره در حافظه بجای save_virtual_workbook
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    now_str = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"soldiers_{item}_{now_str}.xlsx"

    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response



def support_page(request):
    return render(request,'support_page.html')