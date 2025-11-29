from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from soldires_apps.models import Soldier
from units_apps.models import SubUnit
from .models import ClearanceLetter, NormalLetter, NormalLetterMentalHealthAssessmentAndEvaluation, \
    NormalLetterJudicialInquiry, NormalLetterDomesticSettlement, IntroductionLetter,IntroductionLetterType, MembershipCertificate, \
    NormalLetterHealthIodine, NormalLetterCommitmentLetter
from .forms import ClearanceLetterForm, NormalLetterJudicialInquiryForm, NormalLetterDomesticSettlementForm, \
    IntroductionLetterForm, MembershipCertificateForm, HealthIodineForm, CommitmentLetterForm , EssentialFormCardLetter,EssentialFormCardLetterForm  
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .constants import *
from django.db.models import Q
from django.utils import timezone
from .forms import EssentialFormCardLetterForm
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.db.models.functions import Cast
from django.db.models.expressions import RawSQL
from django.db.models import TextField
import json


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

        # --- فیلتر جستجوی متن ---
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(letter_number__icontains=query) |
                Q(soldier__first_name__icontains=query) |
                Q(soldier__last_name__icontains=query) |
                Q(soldier__national_code__icontains=query)
            )

        # --- فیلتر وضعیت ---
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # --- فیلتر علت ---
        reason = self.request.GET.get('reason')
        if reason:
            queryset = queryset.filter(reason=reason)

        # --- فیلتر بازه تاریخ ---
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from:
            queryset = queryset.filter(expired_file_number_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(expired_file_number_date__lte=date_to)

        # مرتب‌سازی
        return queryset.order_by('-expired_file_number')


def approved_ClearanceLetter(request, letter_id):
    letter = ClearanceLetter.objects.get(id=letter_id)
    if letter.status == 'چاپ و درحال بررسی':
        letter.status = 'تایید شده'
        letter.save()
        
        # Signal خودکار وضعیت سرباز را تغییر می‌دهد
        soldier = letter.soldier
        messages.success(request, f"نامه با موفقیت تایید شد و وضعیت سرباز به '{soldier.get_status_display()}' تغییر یافت.")
    return redirect('ClearanceLetterListView')

import jdatetime

def to_shamsi(gregorian_date):
    if gregorian_date:
        shamsi_date = jdatetime.date.fromgregorian(date=gregorian_date)
        return shamsi_date.strftime("%Y/%m/%d")
    return ""

def print_ClearanceLetter(request, letter_id):
    letter = ClearanceLetter.objects.get(id=letter_id)

    if letter.status == 'ایجاد شده':
        letter.status = 'چاپ و درحال بررسی'
        letter.save()
        messages.success(request, "وضعیت نامه به 'چاپ و درحال بررسی' تغییر یافت.")
    letter.issue_date_shamsi = to_shamsi(letter.issue_date)
    letter.activities_start_date_shamsi = to_shamsi(letter.soldier.dispatch_date)
    letter.activities_end_date_shamsi = to_shamsi(letter.soldier.dispatch_date)
    letter.service_end_date_shamsi = to_shamsi(letter.soldier.service_end_date)
    letter.service_entry_date_shamsi = to_shamsi(letter.soldier.service_entry_date)
    
    sol = letter.soldier
    if sol.expired_file_number != letter.expired_file_number:
        if not letter.expired_file_number:
            letter.expired_file_number = sol.expired_file_number
            letter.save()
            
        else:
            sol.expired_file_number = letter.expired_file_number
            sol.save()    
    
    return render(request, 'soldire_letter_apps/print_ClearanceLetter.html', {'letter': letter})

    
def delete_ClearanceLetter(request, letter_id):
    """حذف نامه تسویه‌حساب و بازگرداندن وضعیت سرباز"""
    letter = get_object_or_404(ClearanceLetter, id=letter_id)
    
    if request.method == 'POST':
        soldier = letter.soldier
        if soldier:
            soldier.is_checked_out = False
            soldier.save()
        # حذف نامه (signal خودکار وضعیت سرباز را تغییر می‌دهد)
        letter.delete()
        
        messages.success(request, f"نامه تسویه‌حساب حذف شد و وضعیت سرباز {soldier.first_name} {soldier.last_name} به 'حین خدمت' بازگردانده شد.")
        return redirect('ClearanceLetterListView')
    
    # نمایش صفحه تایید حذف
    return render(request, 'soldire_letter_apps/delete_ClearanceLetter_confirm.html', {
        'letter': letter,
        'soldier': letter.soldier
    })


def normal_letter_list(request):
    query = request.GET.get('q', '').strip()
    letters = NormalLetter.objects.select_related('soldier')

    if query:
        letters = letters.filter(
            Q(letter_number__icontains=query) |
            Q(letter_type__icontains=query) |
            Q(soldier__first_name__icontains=query) |
            Q(soldier__last_name__icontains=query) |
            Q(soldier__national_code__icontains=query)
        )

    paginator = Paginator(letters.order_by('-created_at'), 100)  # تعداد در هر صفحه = ۲۰
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'letters': page_obj,
        'query': query,
    }
    return render(request, 'soldire_letter_apps/normal_letter_list.html', context)


def create_new_letter_from_old(request, test_id):
    old_test = get_object_or_404(NormalLetterMentalHealthAssessmentAndEvaluation, id=test_id)
    old_soldier = old_test.normal_letter.soldier

    # ساخت نامه جدید
    new_letter = NormalLetter.objects.create(
        soldier=old_soldier,
        letter_type='تست سلامت روان پس از ۶ ماه',
        destination=' قسمت بهداشت و درمان آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه',
        description='تست سلامت روان پس از ۶ ماه',
        created_by=request.user
    )

    # اتصال به مدل تست روان جدید
    NormalLetterMentalHealthAssessmentAndEvaluation.objects.create(
        normal_letter=new_letter,
        subject=old_test.subject
    )

    return redirect('normal_letter_list')


def create_group_mental_health_letters(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_tests')
        created_count = 0

        for test_id in selected_ids:
            try:
                old_test = NormalLetterMentalHealthAssessmentAndEvaluation.objects.get(id=test_id)
                soldier = old_test.normal_letter.soldier

                # بررسی اینکه آیا در 6 ماه گذشته نامه مشابه نداشته
                recent_test = NormalLetterMentalHealthAssessmentAndEvaluation.objects.filter(
                    normal_letter__soldier=soldier,
                    created_at__gte=timezone.now() - timedelta(days=180)
                ).exists()

                if recent_test:
                    continue  # اگر در 6 ماه گذشته نامه دارد، ایجاد نشود

                # ساخت نامه جدید
                new_letter = NormalLetter.objects.create(
                    soldier=soldier,
                    letter_type='تست سلامت روان پس از ۶ ماه',
                    destination=' قسمت بهداشت و درمان آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه',
                    description='تست سلامت روان پس از ۶ ماه',
                    created_by=request.user
                )

                # اتصال تست جدید
                NormalLetterMentalHealthAssessmentAndEvaluation.objects.create(
                    normal_letter=new_letter,
                    subject=old_test.subject
                )

                created_count += 1

            except NormalLetterMentalHealthAssessmentAndEvaluation.DoesNotExist:
                continue

        messages.success(request, f"{created_count} نامه با موفقیت ایجاد شد.")
        return redirect('due_mental_health_letters')


# لیست
def judicial_inquiry_list(request):
    query = request.GET.get('q', '')
    inquiries = NormalLetterJudicialInquiry.objects.select_related('normal_letter__soldier')

    if query:
        inquiries = inquiries.filter(
            Q(normal_letter__letter_number__icontains=query) |
            Q(normal_letter__soldier__first_name__icontains=query) |
            Q(normal_letter__soldier__last_name__icontains=query) |
            Q(normal_letter__soldier__national_code__icontains=query) |
            Q(subject__icontains=query) |
            Q(reason__icontains=query)
        )

    paginator = Paginator(inquiries.order_by('-normal_letter__date'), 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, 'soldire_letter_apps/judicial_inquiry_list.html', {'page_obj': page_obj})


def judicial_inquiry_create(request):
    if request.method == 'POST':
        form = NormalLetterJudicialInquiryForm(request.POST)
        if form.is_valid():
            soldier = form.cleaned_data['soldier']
            reason = form.cleaned_data['reason']
            subject = 'استعلام قضایی'
            description = form.cleaned_data['description']

            # ایجاد نامه نرمال
            normal_letter = NormalLetter.objects.create(
                soldier=soldier,
                letter_type='استعلام قضایی',
                created_by=request.user,
                destination='آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه - مدیریت نیروی انسانی - قضایی و انضباطی ',
                description=description,
            )

            # ایجاد استعلام قضایی
            NormalLetterJudicialInquiry.objects.create(
                normal_letter=normal_letter,
                reason=reason,
                subject=subject,
            )

            return redirect('judicial_inquiry_list')
    else:
        form = NormalLetterJudicialInquiryForm()
    return render(request, 'soldire_letter_apps/judicial_inquiry_form.html',
                  {'form': form, 'title': 'ایجاد استعلام قضایی'})


# ویرایش
def judicial_inquiry_edit(request, pk):
    inquiry = get_object_or_404(NormalLetterJudicialInquiry, pk=pk)
    if request.method == 'POST':
        form = NormalLetterJudicialInquiryForm(request.POST, instance=inquiry)
        if form.is_valid():
            form.save()
            messages.success(request, "ویرایش با موفقیت انجام شد.")
            return redirect('judicial_inquiry_list')
    else:
        # سرباز را از normal_letter بخوانیم
        form = NormalLetterJudicialInquiryForm(
            initial={
                'soldier': inquiry.normal_letter.soldier,
                'reason': inquiry.reason,
            },
            instance=inquiry
        )
    return render(request, 'soldire_letter_apps/judicial_inquiry_form.html',
                  {'form': form, 'title': 'ویرایش استعلام قضایی'})


# حذف
def judicial_inquiry_delete(request, pk):
    inquiry = get_object_or_404(NormalLetterJudicialInquiry, pk=pk)
    if request.method == 'POST':
        inquiry.normal_letter.delete()  # حذف خودکار normal_letter مرتبط هم
        inquiry.delete()
        messages.success(request, "نامه با موفقیت حذف شد.")
        return redirect('judicial_inquiry_list')
    
    return render(request, 'soldire_letter_apps/judicial_inquiry_confirm_delete.html', {'object': inquiry})

def judicial_inquiry_print(request, pk):
    inquiry = get_object_or_404(NormalLetterJudicialInquiry, pk=pk)
    inquiry.normal_letter.destination='آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه - مدیریت نیروی انسانی - قضایی و انضباطی '
    return render(request, 'soldire_letter_apps/print_judicial_inquiry.html', {
        'inquiry': inquiry,
        'letter':inquiry.normal_letter,
        'signature':{
            "name": "میثم گل بابا زاده",
            "degree": "ستوان دوم پاسدار",
            "duty": "کارشناس منابع سرباز",
        }
       
    })


def approved_judicial_inquiry(request, letter_id):
    letter = ClearanceLetter.objects.get(id=letter_id)
    if letter.status == 'چاپ و درحال بررسی':
        letter.status = 'تایید شده'
        letter.save()
        return reverse_lazy('ClearanceLetterListView')


def print_judicial_inquiry(request, letter_id):
    letter = ClearanceLetter.objects.get(id=letter_id)
    if letter.status == 'ایجاد شده':
        letter.status = 'چاپ و درحال بررسی'
        letter.save()
    return render(request, 'soldire_letter_apps/print_judicial_inquiry.html', {'letter': letter})


def domestic_settlement_list(request):
    query = request.GET.get('q', '')
    domestic_settlement = NormalLetterDomesticSettlement.objects.filter().all()

    if query:
        domestic_settlement = domestic_settlement.filter(
            Q(normal_letter__letter_number__icontains=query) |
            Q(normal_letter__soldier__first_name__icontains=query) |
            Q(normal_letter__soldier__last_name__icontains=query) |
            Q(normal_letter__soldier__national_code__icontains=query) |
            Q(subject__icontains=query) |
            Q(reason__icontains=query)
        )

    paginator = Paginator(domestic_settlement.order_by('-normal_letter__date'), 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, 'soldire_letter_apps/domestic_settlement_list.html', {'page_obj': page_obj})


def domestic_settlement_create(request):
    if request.method == 'POST':
        form = NormalLetterDomesticSettlementForm(request.POST)
        if form.is_valid():
            soldier = form.cleaned_data['soldier']
            reason = form.cleaned_data['reason']
            subject = 'تسویه حساب داخلی'
            description = form.cleaned_data['description']

            part = soldier.current_parent_unit
            sub = soldier.current_sub_unit
            # ایجاد نامه نرمال
            normal_letter = NormalLetter.objects.create(
                soldier=soldier,
                letter_type='تسویه حساب داخلی',
                created_by=request.user,
                destination=F'آموزشگاه رزم مقدماتی المهدی(عج) نیروی زمینی سپاه - {part} - {sub}',
                description=description,
            )

            # ایجاد استعلام قضایی
            NormalLetterDomesticSettlement.objects.create(
                normal_letter=normal_letter,
                reason=reason,
                subject=subject,
            )

            return redirect('domestic_settlement_list')
    else:
        form = NormalLetterDomesticSettlementForm()
    return render(request, 'soldire_letter_apps/domestic_settlement_form.html',
                  {'form': form, 'title': 'ایجاد نامه توسیه حساب داخلی'})


def domestic_settlement_delete(request, pk):
    settlement = get_object_or_404(NormalLetterDomesticSettlement, pk=pk)
    if request.method == 'POST':
        settlement.normal_letter.delete()  # حذف خودکار normal_letter مرتبط
        settlement.delete()
        messages.success(request, "نامه با موفقیت حذف شد.")
        return redirect('domestic_settlement_list')
    
    return render(request, 'soldire_letter_apps/domestic_settlement_delete.html', {'settlement': settlement})

def approved_domestic_settlement(request, letter_id):
    domestic_settlement = NormalLetterDomesticSettlement.objects.get(normal_letter_id=letter_id)
    letter = NormalLetter.objects.get(id=domestic_settlement.normal_letter.id)
    find_soldire = Soldier.objects.get(pk=domestic_settlement.normal_letter.soldier.id)
    if letter.status == 'چاپ و درحال بررسی':
        letter.status = 'تایید شده'
        letter.save()
        find_soldire.current_parent_unit = None
        find_soldire.current_sub_unit = None
        find_soldire.save()
    return redirect('domestic_settlement_list')


def print_domestic_settlement(request, letter_id):
    letter = NormalLetterDomesticSettlement.objects.get(normal_letter__id=letter_id)
    if letter and letter.normal_letter.status == 'ایجاد شده':
        letter.normal_letter.status = 'چاپ و درحال بررسی'
        letter.normal_letter.save()
    
    s = letter.normal_letter.soldier
    if s:
        part = s.current_parent_unit.name
        sub = s.current_sub_unit.name
        letter.normal_letter.destination = f'آموزشگاه رزم مقدماتی المهدی(عج) نیروی زمینی سپاه - {part} - {sub}'
        
        
        print(letter.normal_letter.destination)
    return render(request, 'soldire_letter_apps/print_domestic_settlement.html', {
        'letter': letter.normal_letter,
        'domestic_settlement':letter
    })


def introduction_letter_list(request):
    query = request.GET.get('q', '')
    letters = IntroductionLetter.objects.all()

    if query:
        letters = letters.filter(
            Q(letter_number__icontains=query) |
            Q(soldier__national_code__icontains=query) |
            Q(soldier__first_name__icontains=query) |
            Q(soldier__last_name__icontains=query)
        )

    paginator = Paginator(letters.order_by('-created_at'), 10)  # 10 نامه در هر صفحه
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'soldire_letter_apps/introduction_letter_list.html', {
        'page_obj': page_obj,
        'query': query,
    })


def introduction_letter_create(request):
    letter_type = request.GET.get('letter_type', '') or request.GET.get('letter_type', '')
    
    if request.method == 'POST':
        form = IntroductionLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('introduction_letter_list')
    else:
        form = IntroductionLetterForm({
            'letter_type': letter_type or 'معرفی‌نامه'
        })
        form.fields['soldier'].queryset = Soldier.objects.filter(current_sub_unit__isnull=True,
                                                                 current_parent_unit__isnull=True).all()
    
    return render(request, 'soldire_letter_apps/introduction_letter_form.html', {
        'form': form,
        'letter_type':letter_type,
    })


def introduction_letter_create(request):
    if request.method == 'POST':
        form = IntroductionLetterForm(request.POST)
        force_submit = request.POST.get('force_submit') == 'true'

        if form.is_valid():
            part = form.cleaned_data['part']
            soldier = form.cleaned_data['soldier']
            sub_part = form.cleaned_data['sub_part']

            if sub_part and sub_part.HealthIodine:
                has_clearance = NormalLetterHealthIodine.objects.filter(
                    part=part,
                    sub_part=sub_part,
                    normal_letter__soldier=soldier,
                    normal_letter__status='تایید شده'
                ).exists()

                if not has_clearance and not force_submit:
                    messages.warning(
                        request,
                        f"برای معرفی به قسمت «{part.name}» نیاز به تاییدیه سلامت است و این سرباز هنوز آن را ندارد. "
                        f"در صورت تمایل می‌توانید با تأیید دستی ادامه دهید."
                    )
                    return render(request, 'soldire_letter_apps/introduction_letter_form.html', {
                        'form': form,
                        'show_force_submit': True  # نشون می‌ده دکمه تایید دستی باید نمایش داده بشه
                    })

            # ذخیره‌سازی نهایی
            form.save()
            messages.success(request, "نامه معرفی با موفقیت ثبت شد.")
            return redirect('introduction_letter_list')

    else:
        form = IntroductionLetterForm()
        form.fields['soldier'].queryset = Soldier.objects.filter(
            is_checked_out=False,
        )

    return render(request, 'soldire_letter_apps/introduction_letter_form.html', {'form': form})


def introduction_letter_update(request, pk):
    letter = get_object_or_404(IntroductionLetter, pk=pk)
    if request.method == 'POST':
        form = IntroductionLetterForm(request.POST, instance=letter)
        if form.is_valid():
            form.save()
            return redirect('introduction_letter_list')
    else:
        form = IntroductionLetterForm(instance=letter)
    return render(request, 'soldire_letter_apps/introduction_letter_form.html', {'form': form})


def introduction_letter_delete(request, pk):
    letter = get_object_or_404(IntroductionLetter, pk=pk)
    if request.method == 'POST':
        find_soldire = Soldier.objects.get(pk=letter.soldier.id)
        find_soldire.current_parent_unit = None
        find_soldire.current_sub_unit = None
        find_soldire.save()
        letter.delete()
        return redirect('introduction_letter_list')
    return render(request, 'soldire_letter_apps/introduction_letter_confirm_delete.html', {'letter': letter})


def approved_introduction_letter(request, letter_id):
    # اگر رکورد وجود نداشت، 404 نشان داده می‌شود
    introduction_letter = get_object_or_404(IntroductionLetter, pk=letter_id)
    soldier = introduction_letter.soldier

    if introduction_letter.status == 'چاپ و درحال بررسی':
        introduction_letter.status = 'تأیید نهایی'
        introduction_letter.save()

        soldier.current_parent_unit = introduction_letter.part
        soldier.current_sub_unit = introduction_letter.sub_part
        soldier.save()

    return redirect('introduction_letter_list')

def print_introduction_letter(request, letter_id):
    letter = IntroductionLetter.objects.get(id=letter_id)
    if letter.status == 'ایجاد شده':
        letter.status = 'چاپ و درحال بررسی'
        letter.save()

    i = letter.letter_type in   [IntroductionLetterType.I.value,IntroductionLetterType.L5I.value]
    l5 = letter.letter_type in [IntroductionLetterType.L5.value,IntroductionLetterType.L5I.value]  

    if letter:
        letter.date = letter.letter_date
        letter.letter_type = IntroductionLetterType.I.value
        letter.sub_part_of = letter.sub_part or '!زیر قسمت انتخاب نشده!'
        letter.part_of = '!قسمت انتخاب نشده!'
        if letter.sub_part:
            letter.part_of = letter.sub_part.parent_unit or '!قسمت انتخاب نشده!'
                
        letter.destination = f"آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه - مدیریت {letter.part_of}"
    
    refrence_destination = f"آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه - مدیریت نیروی انسانی - منابع سرباز"
    
    
    return render(request, 'soldire_letter_apps/print_introduction_letter.html', {
        'letter': letter,
        'i':i,
        'l5':l5,
        'L5_documents':L5_documents,
        'refrence_destination':refrence_destination,
    })


# دریاف قسمت وزیر قسمت برای معرفی نامه
def load_sub_units(request):
    part_id = request.GET.get('part')
    sub_units = SubUnit.objects.filter(parent_unit_id=part_id).all()
    return render(request, 'soldire_letter_apps/subunit_dropdown_list_options.html', {'sub_units': sub_units})


# لیست گواهی‌ها
def membership_certificate_list(request):
    certificates = MembershipCertificate.objects.all()
    return render(request, 'soldire_letter_apps/certificates_list.html', {'certificates': certificates})


# ایجاد گواهی جدید
def membership_certificate_create(request):
    if request.method == 'POST':
        form = MembershipCertificateForm(request.POST)
        if form.is_valid():
            soldier = form.cleaned_data['soldier']
            destination = form.cleaned_data['final_destination']

            # ساخت نامه عادی با مشخصات
            normal_letter = NormalLetter.objects.create(
                soldier=soldier,
                destination=destination,
                letter_type='گواهی',  # مشخص کردن نوع نامه
                created_by=request.user if request.user.is_authenticated else None
            )

            # ساخت گواهی عضویت و اتصال به نامه
            cert = form.save(commit=False)
            cert.normal_letter = normal_letter
            cert.save()

            return redirect('membership_certificate_list')
    else:
        form = MembershipCertificateForm()

    return render(request, 'soldire_letter_apps/certificates_form.html', {'form': form})


# ویرایش گواهی
def membership_certificate_edit(request, pk):
    cert = get_object_or_404(MembershipCertificate, pk=pk)
    normal_letter = cert.normal_letter
    initial_data = {}

    # بررسی اینکه مقصد داخل لیست هست یا نه
    all_destinations = NormalLetter.objects.values_list('destination', flat=True).distinct()
    if normal_letter.destination in all_destinations:
        initial_data['destination_choice'] = normal_letter.destination
    else:
        initial_data['destination_choice'] = 'custom'
        initial_data['destination_manual'] = normal_letter.destination

    if request.method == 'POST':
        form = MembershipCertificateForm(request.POST, instance=cert)
        if form.is_valid():
            destination = form.cleaned_data['final_destination']
            normal_letter.destination = destination
            normal_letter.save()
            form.save()
            return redirect('membership_certificate_list')
    else:
        form = MembershipCertificateForm(instance=cert, initial=initial_data)

    return render(request, 'soldire_letter_apps/certificates_form.html', {'form': form})


# حذف گواهی
def membership_certificate_delete(request, pk):
    certificate = get_object_or_404(MembershipCertificate, pk=pk)
    if request.method == 'POST':
        certificate.delete()
        return redirect('membership_certificate_list')
    return render(request, 'soldire_letter_apps/certificates_delete_confirm.html', {'certificate': certificate})

def membership_certificate_print(request, pk):
    certificate = get_object_or_404(MembershipCertificate, pk=pk)

    if certificate:
        letter = certificate.normal_letter
        letter.subject = certificate.subject or letter.subject
    context = {
        'certificate': certificate,
        'letter': letter,
        'signature':{
            "name": "علی متولی طاهر",
            "degree": "سرهنگ پاسدار",
            "duty": "فرمانده",
        }
    }
    return render(request, 'soldire_letter_apps/print_membership_certificate.html', context)

def health_iodine_letter_list(request):
    query = request.GET.get('q', '')
    letters = NormalLetterHealthIodine.objects.all()

    if query:
        letters = letters.filter(
            Q(normal_letter__letter_number__icontains=query) |
            Q(normal_letter__soldier__national_code__icontains=query) |
            Q(normal_letter__soldier__first_name__icontains=query) |
            Q(normal_letter__soldier__last_name__icontains=query)
        )

    paginator = Paginator(letters.order_by('-normal_letter__created_by'), 100)  # 10 نامه در هر صفحه
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'soldire_letter_apps/health_iodine_letter_list.html', {
        'page_obj': page_obj,
        'query': query,
    })


# ایجاد نامه تائیدیه سلامت
def health_iodine_letter_create(request):
    if request.method == 'POST':
        form = HealthIodineForm(request.POST)
        if form.is_valid():
            soldier = form.cleaned_data['soldier']
            # ایجاد نامه عادی مرتبط
            normal_letter = NormalLetter.objects.create(
                soldier=soldier,
                destination='آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه - قسمت بهداری',
                letter_type='دریافت تائیدیه سلامت',
                created_by=request.user if request.user.is_authenticated else None
            )
            
            # ذخیره فرم Health Iodine
            hi_letter = form.save(commit=False)
            hi_letter.normal_letter = normal_letter
            hi_letter.save()
            messages.success(request, "نامه تائیدیه سلامت با موفقیت ایجاد شد.")
            return redirect('health_iodine_letter_list')
    else:
        form = HealthIodineForm()
        form.fields['soldier'].queryset = Soldier.objects.all()

    return render(request, 'soldire_letter_apps/health_iodine_letter_form.html', {'form': form})

# بروزرسانی نامه تائیدیه سلامت
def health_iodine_letter_update(request, pk):
    hi_letter = get_object_or_404(NormalLetterHealthIodine, pk=pk)
    if request.method == 'POST':
        form = HealthIodineForm(request.POST, instance=hi_letter)
        if form.is_valid():
            form.save()
            messages.success(request, "نامه تائیدیه سلامت با موفقیت بروزرسانی شد.")
            return redirect('health_iodine_letter_list')
    else:
        form = HealthIodineForm(instance=hi_letter)

    return render(request, 'soldire_letter_apps/health_iodine_letter_form.html', {'form': form})

def health_iodine_letter_delete(request, pk):
    letter = get_object_or_404(NormalLetterHealthIodine, pk=pk)
    
    if request.method == 'POST':
        # حذف normal_letter مرتبط قبل از حذف letter
        if letter.normal_letter:
            letter.normal_letter.delete()
        
        letter.delete()
        messages.success(request, "نامه با موفقیت حذف شد.")
    
    return redirect('health_iodine_letter_list')


def print_health_iodine(request, letter_id):
    letter = NormalLetterHealthIodine.objects.get(id=letter_id)
    
    return render(request, 'soldire_letter_apps/print_health_iodine.html', {'letter': letter.normal_letter , 'health_letter':letter})

def commitment_letter_list(request):
    query = request.GET.get('q', '')
    letters = NormalLetterCommitmentLetter.objects.all()

    if query:
        letters = letters.filter(
            Q(normal_letter__letter_number__icontains=query) |
            Q(normal_letter__soldier__national_code__icontains=query) |
            Q(normal_letter__soldier__first_name__icontains=query) |
            Q(normal_letter__soldier__last_name__icontains=query)
        )

    paginator = Paginator(letters.order_by('-normal_letter__created_by'), 100)  # 10 نامه در هر صفحه
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'soldire_letter_apps/commitment_letter_list.html', {
        'page_obj': page_obj,
        'query': query,
    })


def commitment_letter_create(request):
    if request.method == 'POST':
        form = CommitmentLetterForm(request.POST)
        if form.is_valid():
            soldier = form.cleaned_data['soldier']
            normal_letter = NormalLetter.objects.create(
                soldier=soldier,
                destination='داخلی',
                letter_type='تعهد نامه',
                created_by=request.user if request.user.is_authenticated else None
            )
            cl = form.save(commit=False)
            cl.normal_letter = normal_letter
            cl.save()
            return redirect('commitment_letter_list')
    else:
        form = CommitmentLetterForm()
        form.fields['soldier'].queryset = Soldier.objects.filter().all()
    return render(request, 'soldire_letter_apps/commitment_letter_form.html', {'form': form})


def commitment_letter_update(request, pk):
    letter = get_object_or_404(NormalLetterCommitmentLetter, pk=pk)
    if request.method == 'POST':
        form = CommitmentLetterForm(request.POST, instance=letter)
        if form.is_valid():
            form.save()
            return redirect('commitment_letter_list')
    else:
        form = CommitmentLetterForm(instance=letter)
        soldier = letter.normal_letter.soldier
        form.fields['soldier'].initial = soldier
        form.fields['soldier'].disabled = True
    return render(request, 'soldire_letter_apps/commitment_letter_form.html', {'form': form})


# برسی برای حذف نامه
def commitment_letter_delete(request, pk):
    return render(request, 'soldire_letter_apps/commitment_letter_form.html', )


def commitment_letter_print(request, pk):
    letter = get_object_or_404(NormalLetterCommitmentLetter, pk=pk)
    letter.activities_start_date_shamsi = to_shamsi(letter.normal_letter.soldier.dispatch_date)
    letter.service_entry_date_shamsi = to_shamsi(letter.normal_letter.soldier.service_entry_date)
    return render(request, 'soldire_letter_apps/print_commitment_letter.html', {'letter':letter})


def approved_commitment_letter(request, letter_id):
    commitment_letter = NormalLetterCommitmentLetter.objects.get(id=letter_id)
    find_soldire = Soldier.objects.get(pk=commitment_letter.normal_letter.soldier.id)
    if commitment_letter.status == 'چاپ و درحال بررسی':
        commitment_letter.status = 'تأیید نهایی'
        commitment_letter.save()
        find_soldire.card_chip = commitment_letter.type_card_chip
        find_soldire.save()
    return redirect('commitment_letter_list')


def print_commitment_letter(request, letter_id):
    letter = IntroductionLetter.objects.get(id=letter_id)
    if letter.status == 'ایجاد شده':
        letter.status = 'چاپ و درحال بررسی'
        letter.save()
        letter.date = letter.letter_date
    return render(request, 'soldire_letter_apps/print_commitment_letter.html', {'letter': letter})


def main_letters(request):
    return render(request, 'index.html')
    



def forms_essential_list(request):
    search = request.GET.get("search", "")
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 5))

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    # همه رکوردها قبل از فیلتر
    full_queryset = EssentialFormCardLetter.objects.all()
    total_items = full_queryset.count()  # ✅ تعداد کل رکوردها

    query = full_queryset

    # فیلتر جستجو
    if search:
        query = query.filter(
            Q(title__icontains=search) |
            Q(number__icontains=search) |
            Q(form_data__first_name__icontains=search) |
            Q(form_data__last_name__icontains=search) |
            Q(form_data__national_code__icontains=search)
        )

    # فیلتر تاریخ
    if start_date:
        query = query.filter(created_at__date__gte=parse_date(start_date))

    if end_date:
        query = query.filter(created_at__date__lte=parse_date(end_date))

    # ✅ تعداد نتایج بعد از جستجو
    filtered_items_count = query.count()

    # صفحه‌بندی + convert json
    forms = query.loads_data().paginate(page=page, per_page=per_page)

    # ✅ تعداد آیتم‌هایی که همین صفحه نمایش داده
    current_page_items = len(forms)

    letter_types = EssentialFormCardLetter.LETTER_TYPES

    return render(request, 'essential_forms_nezsa/forms_essential_list.html', {
        'letter_types': letter_types,
        'forms': forms,
        'search': search,
        'start_date': start_date,
        'end_date': end_date,

        # ✅ آمار نمایش به قالب
        'total_items': total_items,
        'filtered_items_count': filtered_items_count,
        'current_page_items': current_page_items,
    })


def form_essential_delete(request,form_id=None): 
    instance = get_object_or_404(EssentialFormCardLetter, pk=form_id)
    print(instance)
    if instance:
        instance.delete()
    return redirect('forms_essential_list')

def form_essential_view(request, form_id=None):
    instance = get_object_or_404(EssentialFormCardLetter, pk=form_id)

    # انتخاب template بر اساس letter_type
    template = 'essential_forms_nezsa/404.html'
    ltype = None
    if instance:
        ltype = instance.letter_type
        page = ltype
        template = f'essential_forms_nezsa/prints/print_{page}.html'

    # تبدیل JSON به dataclass
    form_class = FORM_CLASSES.get(ltype)
    form_data_obj = None
    if form_class and instance.form_data:
        try:
            
            data_dict = json.loads(instance.form_data)
            form_data_obj = form_class(**data_dict)
        except Exception as e:
            print("Error deserializing form_data:", e)
            form_data_obj = None

    context = { 
        'letter': instance,
        'form_data': form_data_obj, 
        'FIELD_LABELS':FIELD_LABELS,
    }

    return render(request, template, context)
from django.shortcuts import get_object_or_404

def form_essential_form(request, form_type, form_id=None):
    if form_id:
        instance = get_object_or_404(EssentialFormCardLetter, pk=form_id)
    else:
        instance = None

    if request.method == "POST":
        form = EssentialFormCardLetterForm(
            request.POST, request.FILES, 
            instance=instance, 
            form_type=form_type
        )
        if form.is_valid():
            form.save()
            return redirect('forms_essential_list')
    else:
        form = EssentialFormCardLetterForm(instance=instance, form_type=form_type)

    
    form_title = FORM_TYPE_TITLES.get(form_type, "فرم")
    
    context = {
        "form": form,
        "form_type": form_type,
        "form_title": form_title,
        'FORM_TYPE_TITLES': FORM_TYPE_TITLES
    }
    return render(request, "essential_forms_nezsa/form_essential_form.html", context)


from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ReadyForms
from .forms import ReadyFormsForm

class ReadyFormsListView(TemplateView):
    template_name = 'ready_forms_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms_list'] = ReadyForms.objects.all().order_by('-created_at')
        context['form'] = ReadyFormsForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'create_form' in request.POST:
            form = ReadyFormsForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "فرم با موفقیت ایجاد شد.")
                return redirect('ready_forms:list')
        elif 'update_form' in request.POST:
            pk = request.POST.get('form_id')
            instance = get_object_or_404(ReadyForms, pk=pk)
            form = ReadyFormsForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, "فرم با موفقیت بروزرسانی شد.")
                return redirect('ready_forms:list')
        return self.get(request, *args, **kwargs)

class ReadyFormsCreateView(TemplateView):
    template_name = 'ready_forms_page.html'

class ReadyFormsUpdateView(TemplateView):
    template_name = 'ready_forms_page.html'

class ReadyFormsDeleteView(TemplateView):
    template_name = 'ready_forms_page.html'

    def get(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(ReadyForms, pk=pk)
        instance.delete()
        messages.success(request, "فرم با موفقیت حذف شد.")
        return redirect('ready_forms:list')


from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils.timezone import now
from .forms import RunawayLetterForm,RunawaySearchForm
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from .models import RunawayLetter

def runaway_page(request):
    form = RunawayLetterForm()
    search_form = RunawaySearchForm(request.GET or None)

    items = RunawayLetter.objects.all().order_by("-created_at")
    if search_form.is_valid():
        print(search_form.cleaned_data)
        items = search_form.filter_queryset(items)

    if request.method == "POST":
        form = RunawayLetterForm(request.POST)
        if form.is_valid():
            runaway = form.save(commit=False)
            runaway.save()
            return redirect("runaway_page")

    # Pagination
    paginator = Paginator(items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "search_form": search_form,
        "page_obj": page_obj,
    }
    return render(request, "soldire_letter_apps/runaway_letter_page.html", context)


def runaway_change_status(request, pk, status):
    """
    تغییر وضعیت نامه فرار و به‌روزرسانی وضعیت سرباز
    """
    valid_statuses = [
        'تأیید نهایی',
        'چاپ و درحال بررسی',
        'ایجاد شده',
    ]

    if status not in valid_statuses:
        return redirect("runaway_page")

    runaway = get_object_or_404(RunawayLetter, pk=pk)

    with transaction.atomic():
        runaway.status = status
        runaway.save()
      

    return redirect("runaway_page")

def runaway_print_page(request, pk):
    """
     صفحه چاپ یک نامه فراری خاص
    """
    runaway_letter = get_object_or_404(RunawayLetter, pk=pk)

    if runaway_letter and runaway_letter.status == 'ایجاد شده':
        runaway_letter.status = 'چاپ و درحال بررسی'
        runaway_letter.save()

    context= {
        'runaway_letter':runaway_letter,
        'letter': runaway_letter.normal_letter,
        'signature':{
            "name": "میثم گل بابا زاده",
            "degree": "ستوان دوم پاسدار",
            "duty": "کارشناس منابع سرباز",
        }
    }
    return render(request, 'soldire_letter_apps/print_runaway_letter.html', context)

def runaway_delete(request, pk):
    runaway = get_object_or_404(RunawayLetter, pk=pk)

    if runaway.normal_letter:
        runaway.normal_letter.delete()

    runaway.delete()

    messages.success(request, "نامه با موفقیت حذف شد.")
    return redirect("runaway_page")



from django.http import HttpResponse
from .enums import ClearanceLetterEnum
from almahdiapp.utils.excel import ExcelExporter,ExcelImport
from almahdiapp.utils.builder import EnumMetaBuilder

def import_clearanceLetter_sample_excel(request):
    """Download sample Excel file using ExcelExporter"""
    eb = EnumMetaBuilder(ClearanceLetterEnum)
    data = CLEARANCE_LETTER_SAMPLE
    required_fields = [ClearanceLetterEnum.LETTER_NUMBER.label,ClearanceLetterEnum.NATIONAL_CODE.label]
    exporter = ExcelExporter(headers=eb.headers, data=data, required_fields=required_fields)
    bio = exporter.export_to_bytes()
    return ExcelExporter.response(bio, filename="نمونه_نامه_تسویه.xlsx")

def import_clearanceLetter_from_excel(request):
    """
    درون‌ریزی نامه‌های تسویه از فایل اکسل
    """
    if request.method == "POST":
        file = request.FILES.get("file")
        print("➡️ File received:", file)

        if not file:
            messages.error(request, "فایل اکسل ارسال نشده است.")
            return redirect(request.path)

        # ساخت Meta برای ستون‌ها
        eb = EnumMetaBuilder(ClearanceLetterEnum)
        print("➡️ Enum choices:", eb.choices)

        # ایجاد ایمپورتر
        importer = ExcelImport(file=file, choices=eb.choices)

        try:
            print("📥 Reading Excel file...")
            importer.read_file()
            print("✔️ File read successfully.")

            print("🧹 Cleaning data...")
            importer.clean_data()
            print("✔️ Clean data completed.")

        except Exception as e:
            print("❌ ERROR while reading/cleaning Excel:", e)
            messages.error(request, f"خطا در خواندن فایل اکسل: {e}")
            return redirect(request.path)

        # رکوردهای تمیزشده
        records = importer.records
        print(f"📊 Cleaned Records Count: {len(records)}")
        print("📊 Sample Record:", records[0] if records else "No records")

        # پردازش رکوردها
        print("⚙️ Running ClearanceLetter.import_data() ...")
        result = ClearanceLetter.import_data(records)
        print("✔️ Import Result:", result)

        # پیام موفقیت
        messages.success(
            request,
            f"درون‌ریزی انجام شد. {result['created']} مورد ایجاد، {result['updated']} مورد بروزرسانی شد."
        )

        # نمایش خطاها اگر وجود داشت
        if result["errors"]:
            print("❌ Errors during import:")
            for err in result["errors"]:
                print("   Record:", err["record"])
                print("   Error:", err["error"])

            messages.error(request, f"{len(result['errors'])} خطا هنگام پردازش رکوردها رخ داد.")

    return redirect('ClearanceLetterListView')
