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

@login_required
def home(request):
    soldires = Soldier.objects.filter(is_checked_out=False)
    allCount = Soldier.objects.all().count()
    soldiers_45_to_end = Soldier.date_to_ends(45).count() 
    stats = {
        'all_soldiers': allCount,
        'active_soldiers': soldires.count(),
        'fugitives': soldires.filter(is_fugitive=True).count(),
        'administrative': soldires.filter(status='توجیحی').count(),
        'shifted': soldires.filter(status='حین خدمت').count(),
        'posted': soldires.filter(status='پایان خدمت').count(),
        'transferred': soldires.filter(status='انتقالی').count(),
        'married': soldires.filter(marital_status='متاهل').count(),
        'single': soldires.filter(marital_status='مجرد').count(),
        'with_card': soldires.filter(eligible_for_card_issuance=True).count(),
        'health_status': {
            'salam': soldires.filter(health_status='سالم').count(),
            'exempt': soldires.filter(health_status='معاف از رزم').count(),
            'group_b': soldires.filter(health_status='گروه ب').count(),
            'exempt_group_b': soldires.filter(health_status='معاف+گروه ب').count(),
        },
        'education': {
            'zir_diplom': soldires.filter(degree='زیردیپلم').count(),
            'diplom': soldires.filter(degree='دیپلم').count(),
            'fogh_diplom': soldires.filter(degree='فوق دیپلم').count(),
            'lisans': soldires.filter(degree='لیسانس').count(),
            'fogh_lisans': soldires.filter(degree='فوق لیسانس').count(),
            'doctor': soldires.filter(degree__in=['دکتری', 'دکترا پزشکی']).count(),
        },
        'financial_debt': soldires.filter(file_shortage__isnull=False).exclude(file_shortage='').count(),
        'skill_groups': soldires.values('skill_group').annotate(count=Count('id')),
        'soldiers_45_to_end':soldiers_45_to_end,
    }

    context = {
        'stats': stats,
        'soldires': soldires,
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