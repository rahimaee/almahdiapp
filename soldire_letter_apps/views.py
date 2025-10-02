from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy

from soldires_apps.models import Soldier
from units_apps.models import SubUnit
from .models import ClearanceLetter, NormalLetter, NormalLetterMentalHealthAssessmentAndEvaluation, \
    NormalLetterJudicialInquiry, NormalLetterDomesticSettlement, IntroductionLetter, MembershipCertificate, \
    NormalLetterHealthIodine, NormalLetterCommitmentLetter
from .forms import ClearanceLetterForm, NormalLetterJudicialInquiryForm, NormalLetterDomesticSettlementForm, \
    IntroductionLetterForm, MembershipCertificateForm, HealthIodineForm, CommitmentLetterForm , EssentialFormCardLetter
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


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
    print(letter.soldier.service_end_date,letter.service_end_date_shamsi)
    return render(request, 'soldire_letter_apps/print_ClearanceLetter.html', {'letter': letter})

    
def delete_ClearanceLetter(request, letter_id):
    """حذف نامه تسویه‌حساب و بازگرداندن وضعیت سرباز"""
    letter = get_object_or_404(ClearanceLetter, id=letter_id)
    
    if request.method == 'POST':
        soldier = letter.soldier
        
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
        destination='به : قسمت بهداشت و درمان آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه',
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
                    destination='به : قسمت بهداشت و درمان آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه',
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
                destination='به : قسمت نیروی انسانی آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه - قضایی و انضباطی',
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

            # ایجاد نامه نرمال
            normal_letter = NormalLetter.objects.create(
                soldier=soldier,
                letter_type='تسویه حساب داخلی',
                created_by=request.user,
                destination=F'به : {soldier.current_parent_unit} آموزشگاه رزم مقدماتی المهدی(عج) نیروی زمینی سپاه',
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


# حذف
def domestic_settlement_delete(request, pk):
    inquiry = get_object_or_404(NormalLetterJudicialInquiry, pk=pk)
    if request.method == 'POST':
        inquiry.normal_letter.delete()  # حذف خودکار normal_letter مرتبط هم
        inquiry.delete()
        messages.success(request, "نامه با موفقیت حذف شد.")
        return redirect('domestic_settlement_list')
    return render(request, 'soldire_letter_apps/domestic_settlement_delete.html', {'object': inquiry})


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
    letter = NormalLetter.objects.get(id=letter_id)
    if letter.status == 'ایجاد شده':
        letter.status = 'چاپ و درحال بررسی'
        letter.save()
    return render(request, 'soldire_letter_apps/print_domestic_settlement.html', {'letter': letter})


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
    if request.method == 'POST':
        form = IntroductionLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('introduction_letter_list')
    else:
        form = IntroductionLetterForm()
        form.fields['soldier'].queryset = Soldier.objects.filter(current_sub_unit__isnull=True,
                                                                 current_parent_unit__isnull=True).all()
    return render(request, 'soldire_letter_apps/introduction_letter_form.html', {'form': form})


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
            current_sub_unit__isnull=True,
            current_parent_unit__isnull=True
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
        
    letter.destination = f'به :  {letter.part}'
    return render(request, 'soldire_letter_apps/print_introduction_letter.html', {'letter': letter})


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

    return render(request, 'soldire_letter_apps/print_membership_certificate.html', {'certificate': certificate,'letter':certificate.normal_letter})


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


def health_iodine_letter_create(request):
    if request.method == 'POST':
        form = HealthIodineForm(request.POST)
        if form.is_valid():
            soldier = form.cleaned_data['soldier']
            normal_letter = NormalLetter.objects.create(
                soldier=soldier,
                destination='به : قسمت بهداری آموزشگاه رزم مقدماتی المهدی (عج) نیروی زمینی سپاه',
                letter_type='دریافت تائیدیه سلامت',
                created_by=request.user if request.user.is_authenticated else None
            )
            hi = form.save(commit=False)
            hi.normal_letter = normal_letter
            hi.save()
            return redirect('health_iodine_letter_list')
    else:
        form = IntroductionLetterForm()
        form.fields['soldier'].queryset = Soldier.objects.filter().all()
    return render(request, 'soldire_letter_apps/health_iodine_letter_form.html', {'form': form})


def health_iodine_letter_update(request, pk):
    letter = get_object_or_404(IntroductionLetter, pk=pk)
    if request.method == 'POST':
        form = IntroductionLetterForm(request.POST, instance=letter)
        if form.is_valid():
            form.save()
            return redirect('health_iodine_letter_list')
    else:
        form = IntroductionLetterForm(instance=letter)
    return render(request, 'soldire_letter_apps/health_iodine_letter_form.html', {'form': form})


def health_iodine_letter_delete(request, pk):
    letter = get_object_or_404(IntroductionLetter, pk=pk)
    if request.method == 'POST':
        form = IntroductionLetterForm(request.POST, instance=letter)
        if form.is_valid():
            form.save()
            return redirect('health_iodine_letter_list')
    else:
        form = IntroductionLetterForm(instance=letter)
    return render(request, 'soldire_letter_apps/health_iodine_letter_form.html', {'form': form})

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
    return render(request, 'soldire_letter_apps/print_commitment_letter.html', {'letter': letter})


def main_letters(request):
    return render(request, 'index.html')
    

from .forms import EssentialFormCardLetterForm


def form_essential_list(request):
    forms = EssentialFormCardLetter.objects.all()
    letter_types = EssentialFormCardLetter.LETTER_TYPES
    ctx = {
        'letter_types':letter_types,
        'forms':forms
    }
    return render(request,'essential_forms_nezsa/form_essential_list.html',ctx)

def form_essential_delete(request,form_id=None): 
    
    return redirect('form_essential_list')

def form_essential_view(request, form_id=None):
    # find form_essential in database
    essential_form = None
    page = '404'
    if essential_form:  # این شرط هیچ وقت True نمی‌شود چون همیشه None است
        page = f'form_essential_{essential_form.letter_type}'

    template = f'essential_forms_nezsa/{page}.html'

    if request.method == "PUT":
        pass

    if request.method == "GET":
        pass

    return render(request, template)

def form_essential_create(request, form_type):
    if request.method == "POST":
        form = EssentialFormCardLetterForm(request.POST, form_type=form_type)
        if form.is_valid():
            form.save()
            return redirect('form_essential_list')
    else:
        form = EssentialFormCardLetterForm(form_type=form_type)
    
    return render(request, "essential_forms_nezsa/form_essential_form.html", {"form": form, "form_type": form_type})
