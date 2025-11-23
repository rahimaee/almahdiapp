from django.shortcuts import render
from units_apps.models import ParentUnit,SubUnit
from django.shortcuts import render
from django.utils import timezone
from dateutil.relativedelta import relativedelta 
from persiantools.jdatetime import JalaliDate
from .forms import ReportType2Form
from soldires_apps.models import  Soldier
from .choices import degree_choices, MARITAL_STATUS_CHOICES, HEALTH_STATUS_CHOICES
from django.db.models import Count, Q
from django.conf import settings
import os
from django.shortcuts import redirect
from .models import EshrafAnalyze
from django.utils.timezone import now

from django.shortcuts import render
from soldires_apps.models import Soldier, Settlement
from datetime import date

def index(request):
    today = date.today()
    # تعداد کل سربازان
    all_soldiers = Soldier.objects.filter(is_checked_out=False)
    all_soldiers_counts = all_soldiers.count()
    # حاضر: سربازانی که پایان خدمت نرسیده‌اند و فراری نیستند
    present_soliders_counts = all_soldiers.filter(is_fugitive=False, service_end_date__gt=today).count()
    # فراری
    runaway_soliders_counts = all_soldiers.filter(is_fugitive=True).count()
    # اعلام حضور نشده: فرضاً سربازانی که هنوز اعزام نشده‌اند یا service_entry_date خالی است
    not_reported_counts = all_soldiers.filter(service_entry_date__isnull=True).count()
    # پایان خدمت
    finished_service_counts = all_soldiers.filter(service_end_date__lte=today).count()
    # درحال صدور کارت
    issuing_card_counts = all_soldiers.filter(eligible_for_card_issuance=True, card_issuance_status__isnull=True).count()
    # بدهی حقوقی
    debt_counts = Settlement.objects.filter(current_debt_rial__gt=0).count()
    # جذبی
    absorption_counts = all_soldiers.filter(absorption=True).count()

    context = {
        'all_soldiers_counts': all_soldiers_counts,
        'present_soliders_counts': present_soliders_counts,
        'runaway_soliders_counts': runaway_soliders_counts,
        'not_reported_counts': not_reported_counts,
        'finished_service_counts': finished_service_counts,
        'issuing_card_counts': issuing_card_counts,
        'debt_counts': debt_counts,
        'absorption_counts': absorption_counts,
    }

    return render(request, 'analystics_index.html', context)

def latest_statistics(request):
   context = {
      'main_stats': {},
      'shift_stats': {},
      'base_stats': {},
   }
   return render(request, 'analystics/latest_statistics_page.html',context)

def reports_all(request):
    units = ParentUnit.objects.all()

    reports = []
    totals = {
        'edu': {
            'under_diploma': 0,
            'diploma': 0,
            'associate': 0,
            'bachelor': 0,
            'master': 0,
            'doctor': 0,
        },
        'health': {
            'healthy': 0,
            'exempt_from_service': 0,
            'group_b': 0,
            'exempt_plus_group_b': 0,
        },
        'commission': 0,
        'marital': {
            'single': 0,
            'married': 0,
        },
        'admin': 0,
        'shift': 0,
        'post': 0,
        'native': 0,
        'non_native': 0,
        'total': 0,
    }

    soldiers = Soldier.objects.filter(is_checked_out=False,is_fugitive=False)
    for unit in units:
        soldiers = soldiers.filter(current_parent_unit=unit)

        row = {
            'unit': unit,
            'edu': {
                'under_diploma': soldiers.filter(degree__in=['زیر دیپلم','زیردیپلم']).count(),
                'diploma': soldiers.filter(degree='دیپلم').count(),
                'associate': soldiers.filter(degree='فوق دیپلم').count(),
                'bachelor': soldiers.filter(degree='لیسانس').count(),
                'master': soldiers.filter(degree='فوق لیسانس').count(),
                'doctor': soldiers.filter(degree__in=['دکترا', 'دکترا پزشکی','دکتری']).count(),
            },
            'health': {
                'healthy': soldiers.filter(health_status='سالم').count(),
                'exempt_from_service': soldiers.filter(health_status='معاف از رزم').count(),
                'group_b': soldiers.filter(health_status='گروه ب').count(),
                'exempt_plus_group_b': soldiers.filter(health_status='معاف+گروه ب').count(),
            },
            'commission': soldiers.filter(status='توجیحی').count(),
            'marital': {
                'single': soldiers.filter(marital_status='مجرد').count(),
                'married': soldiers.filter(marital_status='متاهل').count(),
            },
            'admin': soldiers.filter(traffic_status='اداری').count(),
            'shift': soldiers.filter(traffic_status='شیفتی').count(),
            'post': soldiers.filter(traffic_status='پستی').count(),
            'native': soldiers.filter(residence_province=unit.province).count() if hasattr(unit, 'province') else 0,
            'non_native': soldiers.filter(residence_province__ne=unit.province).count() if hasattr(unit, 'province') else 0,
        }

        row['total'] = sum(row['edu'].values())

        # جمع کل
        for key, value in row['edu'].items():
            totals['edu'][key] += value
        for key, value in row['health'].items():
            totals['health'][key] += value
        totals['commission'] += row['commission']
        for key, value in row['marital'].items():
            totals['marital'][key] += value
        totals['admin'] += row['admin']
        totals['shift'] += row['shift']
        totals['post'] += row['post']
        totals['native'] += row['native']
        totals['non_native'] += row['non_native']
        totals['total'] += row['total']

        reports.append(row)

    context = {
        'reports': reports,
        'totals': totals,
    }

    return render(request, 'analystics/reports_all_page.html', context)


def reports_dagree(request):
    units = ParentUnit.objects.all()

    reports = []
    totals = {
        'officer': {'officer_1': 0, 'officer_2': 0, 'officer_3': 0, 'officer_total': 0},
        'ranked': {'ranked_1': 0, 'ranked_2': 0, 'ranked_3': 0, 'ranked_total': 0},
        'normal': {'normal_1': 0, 'normal_2': 0, 'normal_3': 0, 'normal_4': 0, 'normal_5': 0, 'normal_6': 0},
        'total': 0
    }

    for unit in units:
        soldiers = Soldier.objects.filter(current_parent_unit=unit)

        # دسته‌بندی سربازان بر اساس رده
        officer_1 = soldiers.filter(rank='ستوان یکم(12)').count()
        officer_2 = soldiers.filter(rank='ستوان دوم(11)').count()
        officer_3 = soldiers.filter(rank='ستوان سوم(10)').count()
        officer_total = officer_1 + officer_2 + officer_3

        ranked_1 = soldiers.filter(rank='رزمدار یکم(9)').count()
        ranked_2 = soldiers.filter(rank='رزمدار دوم(8)').count()
        ranked_3 = soldiers.filter(rank='رزم آور یکم(7)').count()
        ranked_total = ranked_1 + ranked_2 + ranked_3

        normal_1 = soldiers.filter(rank='رزم آور دوم(6)').count()
        normal_2 = soldiers.filter(rank='رزم آور سوم(5)').count()
        normal_3 = soldiers.filter(rank='رزمیار(4)').count()
        normal_4 = soldiers.filter(rank='سرباز یکم(3)').count()
        normal_5 = soldiers.filter(rank='سرباز دوم(2)').count()
        normal_6 = soldiers.filter(rank='سرباز(1)').count()
        normal_total = normal_1 + normal_2 + normal_3 + normal_4 + normal_5 + normal_6

        total_unit = officer_total + ranked_total + normal_total

        # جمع‌ها
        totals['officer']['officer_1'] += officer_1
        totals['officer']['officer_2'] += officer_2
        totals['officer']['officer_3'] += officer_3
        totals['officer']['officer_total'] += officer_total

        totals['ranked']['ranked_1'] += ranked_1
        totals['ranked']['ranked_2'] += ranked_2
        totals['ranked']['ranked_3'] += ranked_3
        totals['ranked']['ranked_total'] += ranked_total

        totals['normal']['normal_1'] += normal_1
        totals['normal']['normal_2'] += normal_2
        totals['normal']['normal_3'] += normal_3
        totals['normal']['normal_4'] += normal_4
        totals['normal']['normal_5'] += normal_5
        totals['normal']['normal_6'] += normal_6

        totals['total'] += total_unit

        reports.append({
            'unit': unit,
            'officer': {
                'officer_1': officer_1,
                'officer_2': officer_2,
                'officer_3': officer_3,
                'officer_total': officer_total
            },
            'ranked': {
                'ranked_1': ranked_1,
                'ranked_2': ranked_2,
                'ranked_3': ranked_3,
                'ranked_total': ranked_total
            },
            'normal': {
                'normal_1': normal_1,
                'normal_2': normal_2,
                'normal_3': normal_3,
                'normal_4': normal_4,
                'normal_5': normal_5,
                'normal_6': normal_6
            },
            'total': total_unit
        })

    ctx = {
        'units': units,
        'reports': reports,
        'totals': totals
    }

    return render(request, 'analystics/reports_dagree_page.html', ctx)

def reports_comprehensive(request): 
   return render(request, 'analystics/reports_comprehensive_page.html',)


from persiantools.jdatetime import JalaliDate
from django.db.models import Min, Max
from datetime import date

def reports_ages(request):
    # گرفتن کمترین و بیشترین تاریخ تولد
    birth_minmax = Soldier.objects.aggregate(min_date=Min('birth_date'), max_date=Max('birth_date'))
    min_birth = birth_minmax['min_date']
    max_birth = birth_minmax['max_date']

    # اگر داده وجود نداشت
    if not min_birth or not max_birth:
        return render(request, 'analystics/reports_ages_page.html', {'years_data': [], 'age_data': []})

    # تبدیل به شمسی
    min_year = JalaliDate(min_birth).year
    max_year = JalaliDate(max_birth).year

    # ایجاد دیکشنری برای تعداد متولدین به تفکیک سال
    years_data = {year: 0 for year in range(min_year, max_year+1)}
    
    # محاسبه سن
    today = date.today()
    age_data = {}

    for soldier in Soldier.objects.all():
        j_date = JalaliDate(soldier.birth_date)
        year = j_date.year
        age = today.year - soldier.birth_date.year - ((today.month, today.day) < (soldier.birth_date.month, soldier.birth_date.day))
        years_data[year] += 1

        if age in age_data:
            age_data[age] += 1
        else:
            age_data[age] = 1

    # مرتب سازی
    years_data = dict(sorted(years_data.items()))
    age_data = dict(sorted(age_data.items(), reverse=True))  # سن بالاتر در ابتدای جدول

    # محاسبه میانگین سن
    total_soldiers = sum(age_data.values())
    avg_age = sum(age * count for age, count in age_data.items()) / total_soldiers if total_soldiers else 0

    context = {
        'years_data': years_data,
        'age_data': age_data,
        'avg_age': round(avg_age, 1),
        'total_soldiers': total_soldiers,
    }

    return render(request, 'analystics/reports_ages_page.html', context)


def reports_percent(request):
    total = Soldier.objects.count() or 1  # جلوگیری از تقسیم بر صفر

    # Education counts
    edu_below_diploma = Soldier.objects.filter(degree__in=['زیردیپلم','زیر دیپلم']).count()
    edu_diploma = Soldier.objects.filter(degree='دیپلم').count()
    edu_associate = Soldier.objects.filter(degree='فوق دیپلم').count()
    edu_bachelor = Soldier.objects.filter(degree='لیسانس').count()
    edu_master = Soldier.objects.filter(degree='فوق لیسانس').count()
    edu_phd = Soldier.objects.filter(degree__in=['دکترا','دکتری','دکتر']).count()
    edu_medical_phd = Soldier.objects.filter(degree='دکترا پزشکی').count()

    # Education percentages
    edu_percent_below_diploma = f"{(edu_below_diploma / total * 100):.1f}%"
    edu_percent_diploma = f"{(edu_diploma / total * 100):.1f}%"
    edu_percent_associate = f"{(edu_associate / total * 100):.1f}%"
    edu_percent_bachelor = f"{(edu_bachelor / total * 100):.1f}%"
    edu_percent_master = f"{(edu_master / total * 100):.1f}%"
    edu_percent_phd = f"{(edu_phd / total * 100):.1f}%"
    edu_percent_medical_phd = f"{(edu_medical_phd / total * 100):.1f}%"

    # Health status counts
    health_healthy = Soldier.objects.filter(health_status='سالم').count()
    health_exempt = Soldier.objects.filter(health_status='معاف از رزم').count()
    health_group_b = Soldier.objects.filter(health_status='گروه ب').count()
    health_exempt_group_b = Soldier.objects.filter(health_status='معاف+گروه ب').count()

    # Health percentages
    health_percent_healthy = f"{(health_healthy / total * 100):.1f}%"
    health_percent_exempt = f"{(health_exempt / total * 100):.1f}%"
    health_percent_group_b = f"{(health_group_b / total * 100):.1f}%"
    health_percent_exempt_group_b = f"{(health_exempt_group_b / total * 100):.1f}%"

    # Other statuses counts
    fugitive_count = Soldier.objects.filter(is_fugitive=True).count()
    local_count = Soldier.objects.filter(residence_province__isnull=False).count()
    nonlocal_count = Soldier.objects.filter(residence_province__isnull=True).count()
    commission_count = Soldier.objects.filter(settlement__status='cleared').count()

    # Other statuses percentages
    fugitive_percent = f"{(fugitive_count / total * 100):.1f}%"
    local_percent = f"{(local_count / total * 100):.1f}%"
    nonlocal_percent = f"{(nonlocal_count / total * 100):.1f}%"
    commission_percent = f"{(commission_count / total * 100):.1f}%"

    return render(request, 'analystics/reports_percent_page.html', {
        # Education
        'edu_below_diploma': edu_below_diploma,
        'edu_percent_below_diploma': edu_percent_below_diploma,
        'edu_diploma': edu_diploma,
        'edu_percent_diploma': edu_percent_diploma,
        'edu_associate': edu_associate,
        'edu_percent_associate': edu_percent_associate,
        'edu_bachelor': edu_bachelor,
        'edu_percent_bachelor': edu_percent_bachelor,
        'edu_master': edu_master,
        'edu_percent_master': edu_percent_master,
        'edu_phd': edu_phd,
        'edu_percent_phd': edu_percent_phd,
        'edu_medical_phd': edu_medical_phd,
        'edu_percent_medical_phd': edu_percent_medical_phd,

        # Health
        'health_healthy': health_healthy,
        'health_percent_healthy': health_percent_healthy,
        'health_exempt': health_exempt,
        'health_percent_exempt': health_percent_exempt,
        'health_group_b': health_group_b,
        'health_percent_group_b': health_percent_group_b,
        'health_exempt_group_b': health_exempt_group_b,
        'health_percent_exempt_group_b': health_percent_exempt_group_b,

        # Other statuses
        'fugitive_count': fugitive_count,
        'fugitive_percent': fugitive_percent,
        'local_count': local_count,
        'local_percent': local_percent,
        'nonlocal_count': nonlocal_count,
        'nonlocal_percent': nonlocal_percent,
        'commission_count': commission_count,
        'commission_percent': commission_percent,
    })

def reports_planning(request): 
   units = ParentUnit.objects.all()
   ctx  = {
      'units' : units
   }
   return render(request, 'analystics/reports_planning_page.html',ctx)


def reports_near_end_service(request):
    # تاریخ امروز میلادی (برای محاسبات سرور)
    today = timezone.now().date()

    # تاریخ امروز شمسی (برای نمایش به کاربر)
    today_jalali = JalaliDate(today).strftime("%Y/%m/%d")

    # دریافت تاریخ گزارش از کلاینت (شمسی)
    report_date_jalali = request.GET.get("report_date", today_jalali)

    try:
        # تبدیل تاریخ شمسی ورودی به میلادی
        report_date_gregorian = JalaliDate.strptime(report_date_jalali, "%Y/%m/%d").to_gregorian()
    except Exception:
        report_date_gregorian = today  # اگر ورودی خراب بود، امروز میلادی

    # چند ماه تا پایان خدمت (پیش‌فرض: 3 ماه)
    end_service = int(request.GET.get("end_service", 3))

    # تاریخ حد نهایی (report_date + n ماه) → میلادی
    end_limit = report_date_gregorian + relativedelta(months=+end_service)

    # گرفتن لیست یگان‌ها
    units = ParentUnit.objects.all()

    # شمارش سربازان (اینجا فعلاً صفر استاتیک گذاشتم)
    dynamic_units = []
    for u in units:
        dynamic_units.append({
            "name": u.name,
            "count": 0,  # بعداً اینجا فیلتر سربازها میاد
            "unit": "نفر"
        })

    # یگان‌های استاتیک
    static_units = [
        {"name": "مامور", "count": 0, "unit": "نفر"},
    ]

    all_units = dynamic_units + static_units
    total_count = sum(u["count"] for u in all_units)

    ctx = {
        "report_date": report_date_jalali,  # نمایش در کلاینت فقط شمسی
        "end_service": end_service,
        "units": all_units,
        "total_count": total_count,
    }
    return render(request, "analystics/reports_near_end_service_page.html", ctx)

def reports_skill_training(request): 
       # دیتای آزمایشی (در عمل باید از DB بیاد)
    skills_summary = {
        "no_basic_skills": 0,
        "with_basic_skills": 12,
        "no_skill_cert": 12,
        "with_skill_cert": 0,
        "with_one_cert": 1,
    }

    skill_groups = [
        {"group": "گروه 1 : پزشکی و پیراپزشکی", "requirement": "ندارد", "count": 0, "trained": 0},
        {"group": "گروه 2 : تحصیلات تکمیلی و غیرپزشکی", "requirement": "ندارد", "count": 0, "trained": 0},
        {"group": "گروه 3 : لیسانس", "requirement": "مشروط", "count": 1, "trained": 0},
        {"group": "گروه 4 : فوق دیپلم و دیپلم فنی و حرفه ای و کاردانش", "requirement": "ندارد", "count": 4, "trained": 0},
        {"group": "گروه 5 : فوق دیپلم و دیپلم به پایین", "requirement": "دارد", "count": 14, "trained": 0},
        {"group": "گروه 6 : دارندگان گواهینامه فنی و حرفه ای", "requirement": "ندارد", "count": 0, "trained": 0},
        {"group": "گروه 7 : فوق دیپلم و دیپلم قدیمی", "requirement": "ندارد", "count": 0, "trained": 0},
    ]

    ctx = {
        "skills_summary": skills_summary,
        "skill_groups": skill_groups,
    }
    return render(request, 'analystics/reports_skill_training_page.html',ctx)


def reports_chip(request): 
    chip_stats = {
        "delivered_chips": 0,
        "delivered_cards": 0,
        "without_chip_or_card": 0,
        "present": 0,
        "absent": 0,
        "delivered_total": 0,
        "present_total": 0,
        "list_total": 0,
        "calc_check": 0, 
    }

    ctx = {
        "chip_stats": chip_stats,
    }
    return render(request, "analystics/reports_chip_page.html", ctx)

import jdatetime  # برای تاریخ شمسی
import jdatetime
from collections import defaultdict
from django.db.models import Count, Q
from .choices import RANK_CHOICES_KEYS,RANK_CHOICES,RANK_OFFICER,RANK_DAGREE,RANK_SARBAZ
from datetime import timedelta

def reports_type2(request):
    form = ReportType2Form(request.GET or None)
    if form.is_valid():
        data = form.cleaned_data
        unit = data['unit']
        month = data['month']
        base_date = data['base_date']
        base_date_j = data['base_date_j']
        base_date_g = data['base_date_g']
        next_date_g = data['next_date_g']
    else:
        # fallback به مقادیر پیش‌فرض فرم
        unit = form.default_unit
        month = form.default_month
        base_date = form.default_base_date.strftime('%Y/%m/%d')
        base_date_j = form.default_base_date
        base_date_g = base_date_j.togregorian()
        next_date_g = base_date_g + relativedelta(months=month)

    # واکشی زیرواحدها
    sub_units = SubUnit.objects.filter(parent_unit=unit)

    # سربازانی که تا ماه بعدی تسویه می‌کنند
    soldiers_end_in_days = Soldier.objects.filter(
        is_checked_out=False,
        is_fugitive=False,
        service_end_date__gt=base_date_g,   # بزرگتر از تاریخ مبنا (میلادی)
        service_end_date__lt=next_date_g    # کوچکتر از تاریخ یک ماه بعد (میلادی)
    )
    soldiers_not_end_in_days = Soldier.objects.filter(
        (
           Q(is_checked_out=False) & Q(is_fugitive=False)
           & 
            ( 
                Q(service_end_date__isnull=True) |
                Q(service_end_date__gt=next_date_g) 
            )
        )
    )
    stats = defaultdict(int)
    
    sub_units_data = []
    for sub in sub_units:
        soldiers = soldiers_end_in_days.filter(current_sub_unit=sub)

        # آمار زیرواحد
        sub_stats = {
            'name': sub.name,
            'all': soldiers.count(),
            'salem': soldiers.filter(health_status='سالم').count(),
            'moafazrazm': soldiers.filter(health_status='معاف از رزم').count(),
            'moafazrazmgrohb': soldiers.filter(health_status='گروه ب').count(),
            'moafazrazbamgrohb': soldiers.filter(health_status='معاف+گروه ب').count(),
            'komision': soldiers.filter(health_status='معاف+گروه ب').count(),
            'edari': soldiers.filter(rank__icontains='اداری').count(),
            'shifti': soldiers.filter(rank__icontains='شیفتی').count(),
            'bomi': soldiers.filter(residence_province__isnull=False).count(),
            'bomino': soldiers.filter(residence_province__isnull=True).count(),
            'officer': soldiers.filter(rank__in=RANK_OFFICER).count(),
            'dagree': soldiers.filter(rank__in=RANK_DAGREE).count(),
            'sarbaz': soldiers.filter(rank__in=RANK_SARBAZ).count(),
            'pasdarvazife': soldiers.filter(is_guard_duty=True).count(),
            'zirdiplom': soldiers.filter(degree='زیردیپلم').count(),
            'diplom': soldiers.filter(degree='دیپلم').count(),
            'foghdiplom': soldiers.filter(degree='فوق دیپلم').count(),
            'lisans': soldiers.filter(degree='لیسانس').count(),
            'foghlisans': soldiers.filter(degree='فوق لیسانس').count(),
            'doctor': soldiers.filter(degree__icontains='دکترا').count(),
        }

        # جمع‌بندی برای واحد
        for k, v in sub_stats.items():
            if k != 'name':
                stats[k] += v

        sub_units_data.append(sub_stats)

    # داده نهایی برای قالب
    total_soldiers_counts= soldiers_not_end_in_days.count()
    # درصد سربازان حاضر به کل سربازان
    soldiers_exist_in_unit =  soldiers_not_end_in_days.filter(current_parent_unit=unit).count()  
    percentage_in_unit_counts = (soldiers_exist_in_unit / total_soldiers_counts * 100) if Soldier.objects.exists() else 0
    formatted_percentage = "{:.2f}".format(percentage_in_unit_counts)
    # تعداد ترخیصی‌های قسمت
    unit_discharged_counts = soldiers_end_in_days.filter(current_parent_unit=unit).count()  
    # تعداد ترخیصی‌های آموزشگاه
    academy_discharged_counts = soldiers_end_in_days.count()  

    data = {
        'unit': unit,
        'month': month,
        'base_date': base_date,
        'form':form,
        'sub_units': sub_units_data,
        'unit_stats': stats,
        'total_soldiers_counts':total_soldiers_counts,
        'soldiers_exist_in_unit':soldiers_exist_in_unit,
        'percentage_in_unit_counts':formatted_percentage,
        'unit_discharged_counts':unit_discharged_counts,
        'academy_discharged_counts':academy_discharged_counts,
    }


    ctx = {
        'form': form,
        'data': data
    }

    return render(request, "analystics/reports_type2_page.html", ctx)

from django.shortcuts import render, redirect, get_object_or_404
from .models import EshrafAnalyze
from django.utils.timezone import now
import os
from django.core.files import File

def reports_eshraf(request):
    eshraf_list = EshrafAnalyze.objects.all().order_by("-date")
    selected_id = request.GET.get("selected")
    selected_eshraf = None
    files_list = []  # لیست فایل‌ها

    if selected_id:
        selected_eshraf = get_object_or_404(EshrafAnalyze, id=selected_id)

    # جمع‌آوری فایل‌ها در یک لیست
    file_fields = [
        "file_1", "file_2", "file_3", "file_4", "file_5",
        "file_6", "file_7", "file_8", "file_9", "file_10"
    ]
    for eshraf in eshraf_list:
        files_list = []
        for field in file_fields:
            f = getattr(eshraf, field)
            if f:
                files_list.append({
                    "label": eshraf.RENAME_FILE_LABEL.get(field, f"فایل {field[-1]}"),
                    "name": eshraf.RENAME_FILE_NAME.get(field, f.name),
                    "url": f.url,
                    "ext": f.name.split('.')[-1]  # پسوند فایل
                })
        print(eshraf.title,len(files_list))
        eshraf.files_list = files_list

    return render(request, "analystics/reports_eshraf_page.html", {
        "eshraf_list": eshraf_list,
        "selected_eshraf": selected_eshraf,
    })

import string
import random

def generate_random_filename(ext="xlsx", length=8):
    """نام فایل رندم تولید می‌کند"""
    letters = string.digits
    return "".join(random.choices(letters, k=length)) + f".{ext}"

def generate_random_content(length=100):
    """محتوای رندم برای فایل ایجاد می‌کند"""
    letters = string.ascii_letters + string.digits + " "
    return "".join(random.choices(letters, k=length))

def generate_random_content(length=100):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".txt"
from django.core.files.base import ContentFile

def reports_eshraf_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        date = request.POST.get("date")
        description = request.POST.get("description") or "توضیحات ندارد"
        period = request.POST.get("period")

        eshraf = EshrafAnalyze.objects.create(
            title=title,
            date=date,
            description=description,
            period=period,
        )

        base_path = os.path.join(settings.MEDIA_ROOT, "analystics","eshraf")
        os.makedirs(base_path, exist_ok=True)


        # ایجاد و ذخیره ۱۰ فایل رندم بدون نوشتن روی هارد
        for i in range(1, 11):
            filename = generate_random_filename()
            content = generate_random_content(100)
            getattr(eshraf, f"file_{i}").save(filename, ContentFile(content), save=False)

        eshraf.save()

    return redirect('analystics:reports_eshraf')

def reports_eshraf_delete(request, eshraf_id):
    # دریافت رکورد اشراف
    eshraf = get_object_or_404(EshrafAnalyze, id=eshraf_id)

    # لیست فیلدهای فایل‌ها
    file_fields = [
        eshraf.file_1,
        eshraf.file_2,
        eshraf.file_3,
        eshraf.file_4,
        eshraf.file_5,
        eshraf.file_6,
        eshraf.file_7,
        eshraf.file_8,
        eshraf.file_9,
        eshraf.file_10,
    ]

    # حذف فایل‌ها از دیسک
    for f in file_fields:
        if f and f.name:
            file_path = os.path.join(settings.MEDIA_ROOT, f.name)
            if os.path.exists(file_path):
                os.remove(file_path)

    # حذف رکورد از دیتابیس
    eshraf.delete()

    # بازگشت به صفحه لیست
    return redirect('analystics:reports_eshraf')

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import os
import zipfile
from io import BytesIO
from datetime import datetime


def reports_eshraf_download_zip(request, eshraf_id):
    # دریافت رکورد اشراف
    eshraf = get_object_or_404(EshrafAnalyze, pk=eshraf_id)
    
    # دیکشنری نام دلخواه فایل‌ها
    rename_map = eshraf.RENAME_FILE_NAME
    
    # لیست فیلدهای فایل‌ها
    file_fields = [
        'file_1','file_2','file_3','file_4','file_5',
        'file_6','file_7','file_8','file_9','file_10'
    ]
    
    # ایجاد فایل ZIP در حافظه
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for field_name in file_fields:
            f = getattr(eshraf, field_name)
            if f:
                file_path = os.path.join(settings.MEDIA_ROOT, f.name)
                if os.path.exists(file_path):
                    # پسوند اصلی فایل را نگه می‌داریم
                    original_ext = os.path.splitext(f.name)[1]  # شامل نقطه، مثل ".xlsx"
                    custom_name = rename_map.get(field_name, os.path.basename(f.name))
                    zip_file.write(file_path, custom_name + original_ext)

    zip_buffer.seek(0)
    
    # نام فایل ZIP: عنوان - دوره - تاریخ امروز
    today_str = datetime.now().strftime("%Y-%m-%d")
    zip_filename = f"{eshraf.title} - {eshraf.period} - {today_str}.zip"
    
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
    return response