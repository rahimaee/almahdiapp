from soldires_apps.constants import *
from .dataclass import *
from typing import  Dict,Type

employee_types = [
    ('وظیفه','وظیفه'),
    ('کادر','کادر'),
    ('بسیجی','بسیجی'),
]
card_types = [
    ('المثنی','المثنی'),
    ('مفقودی','مفقودی'),
    ('تعویضی','تعویضی'),
]

FIELD_CHOICES = {
    "rank": RANK_CHOICES,
    "marital_status": MARITAL_STATUS_CHOICES,
    "blood_group": blood_group_choices,
    "education_level": degree_choices,
    'employee_type':employee_types,
    'card_type':card_types,
}

# فرض می‌کنیم کلاس‌ها همان‌هایی هستند که تعریف کردی
FORM_CLASSES: Dict[str, Type] = {
    "clearance_letter": ClearanceLetterFormData,
    "officer_card": OfficerCardFormData,
    "soldier_card": SoldierCardFormData,
    "checkout_3plus": Checkout3PlusFormData,
    "activate_old_staff": ActivateOldStaffFormData,
    "certificate_two_guard": CertificateTwoGuardFormData,
    "permanent_exemption": PermanentExemptionFormData,
}
FORM_TYPE_TITLES = {
    "clearance_letter": "فرم شماره ۳",
    "permanent_exemption": "فرم معافیت دائم کارکنان وظیفه",
    "soldier_card": "فرم صدور کارت سرباز",
    "officer_card": "فرم صدور کارت پایور",
    "checkout_3plus": "فرم تسویه‌حساب ۳ فرزندی و بالاتر",
    "activate_old_staff": "فعال‌سازی اعزام کارکنان قدیمی",
}

# عنوان‌ فارسی برای فیلدهای داینامیک
FIELD_LABELS = {
    "full_name": "نام و نام خانوادگی",
    "father_name": "نام پدر",
    "national_code": "کد ملی",
    "military_code": "کد نظام وظیفه",
    "birth_date": "تاریخ تولد",
    "unit_name": "یگان خدمتی",
    "rank": "درجه",
    "date_start": "تاریخ شروع خدمت",
    "date_end": "تاریخ پایان خدمت",
    "address": "آدرس",
    "phone": "شماره تماس",
    "shkh": "شماره ش.خ",
    "course_name": "نام دوره",
    "course_number": "شماره دوره",
    "attachment_count": "تعداد پیوست",

    "officer_name": "نام پایور",
    "officer_id": "کد ملی / شماره پرسنلی",
    "rank": "درجه",
    "enlistment_date": "تاریخ اعزام",

    "soldier_name": "نام سرباز",
    "soldier_id": "کد ملی / شماره نظامی",
    "unit": "یگان خدمتی",

    "children_count": "تعداد فرزندان",
    "discharge_date": "تاریخ ترخیص",

    "staff_name": "نام کارمند",
    "staff_id": "شماره پرسنلی",
    "birth_year": "سال تولد",

    "first_guard_date": "تاریخ پاسداری اول",
    "second_guard_date": "تاریخ پاسداری دوم",

    "exemption_reason": "علت معافیت",
    "exemption_date": "تاریخ معافیت",

        # اطلاعات پایه
    "first_name": "نام",
    "last_name": "نام خانوادگی",
    "father_name": "نام پدر",
    "birth_certificate_number": "شماره شناسنامه",
    "national_code": "کد ملی",
    "unit_name": "محل خدمت",
    "rank": "درجه",
    "employee_type": "نوع کارمند (کادر، بسیجی، وظیفه)",

    # اطلاعات تکمیلی
    "birth_date": "تاریخ تولد",
    "birth_place": "محل تولد",
    "card_issue_date": "تاریخ صدور کارت",
    "eye_color": "رنگ چشم",
    "blood_group": "گروه خون",
    "height": "قد (سانتی‌متر)",
    "service_branch": "رسته خدمتی",
    "education_level": "مدرک تحصیلی",
    "specialty_code": "کد تخصصی",
    "military_education_status": "وضعیت آموزشی نظامی",
    "legal_service_duration": "مدت قانونی خدمت (ماه)",
    "served_duration": "مدت خدمت انجام شده (ماه)",
    "service_start_date": "تاریخ شروع خدمت",
    "service_end_date": "تاریخ خاتمه خدمت",
    "personal_code": "شماره پرسنلی / کد پاسداری",
    "deployment_area": "حوزه اعزام کننده",
    "main_office_number": "شماره دفتر اساس",
    "detailed_office_number": "شماره دفتر تفضیلی",
    "discharge_unit": "یگان ترخیص‌کننده",

    # اطلاعات فرم
    "card_type": "نوع کارت (المثنی، تعویضی، مفقودی)",
    "subject": "موضوع",
    "sender": "از",
    "receiver": "به",
    "description": "توضیحات اضافی",
    "attachment_count": "تعداد پیوست",
    "main_image": "تصویر اصلی کارت",
    "normal_image": "تصویر نرمال کارت",
}

# متن راهنما برای فیلدهای داینامیک
FIELD_LABELS_HELPER = {
    "full_name": "نام و نام خانوادگی فرد را وارد کنید",
    "father_name": "نام پدر فرد",
    "national_code": "کد ملی را بدون خط تیره وارد کنید",
    "military_code": "شماره نظام وظیفه فرد",
    "birth_date": "تاریخ تولد به فرمت yyyy/mm/dd",
    "unit_name": "نام یگان یا محل خدمت",
    "rank": "درجه نظامی فرد را انتخاب کنید",
    "date_start": "تاریخ شروع خدمت",
    "date_end": "تاریخ پایان خدمت",
    "address": "آدرس محل سکونت",
    "phone": "شماره تماس با کد کشور",
    "shkh": "شماره شناسنامه",
    "course_name": "نام دوره آموزشی",
    "course_number": "شماره دوره آموزشی",
    "attachment_count": "تعداد فایل‌ها یا پیوست‌ها",

    "officer_name": "نام کامل پایور",
    "officer_id": "کد ملی یا شماره پرسنلی پایور",
    "enlistment_date": "تاریخ اعزام به خدمت",

    "soldier_name": "نام کامل سرباز",
    "soldier_id": "کد ملی یا شماره نظامی سرباز",
    "unit": "یگان خدمتی سرباز",

    "children_count": "تعداد فرزندان",
    "discharge_date": "تاریخ ترخیص از خدمت",

    "staff_name": "نام کارمند",
    "staff_id": "شماره پرسنلی کارمند",
    "birth_year": "سال تولد",

    "first_guard_date": "تاریخ پاسداری اول",
    "second_guard_date": "تاریخ پاسداری دوم",

    "exemption_reason": "علت معافیت",
    "exemption_date": "تاریخ صدور معافیت",

    # اطلاعات پایه کارت
    "first_name": "نام فرد",
    "last_name": "نام خانوادگی فرد",
    "birth_certificate_number": "شماره شناسنامه",
    "employee_type": "نوع کارمند: کادر، بسیجی، وظیفه",

    # اطلاعات تکمیلی
    "birth_place": "محل تولد فرد",
    "card_issue_date": "تاریخ صدور کارت",
    "eye_color": "رنگ چشم فرد",
    "blood_group": "گروه خون فرد",
    "height": "قد به سانتی‌متر",
    "service_branch": "رسته خدمتی فرد",
    "education_level": "مدرک تحصیلی فرد",
    "specialty_code": "کد تخصصی فرد",
    "military_education_status": "وضعیت آموزشی نظامی فرد",
    "legal_service_duration": "مدت قانونی خدمت به ماه",
    "served_duration": "مدت خدمت انجام شده به ماه",
    "service_start_date": "تاریخ شروع خدمت",
    "service_end_date": "تاریخ خاتمه خدمت",
    "personal_code": "شماره پرسنلی یا کد پاسداری",
    "deployment_area": "حوزه اعزام کننده",
    "main_office_number": "شماره دفتر اساس",
    "detailed_office_number": "شماره دفتر تفضیلی",
    "discharge_unit": "یگان ترخیص‌کننده",

    # اطلاعات فرم
    "card_type": "نوع کارت: المثنی، تعویضی، مفقودی",
    "subject": "نام سرباز در انتهای موضوع قرار میگیرد.",
    "title": "نام سرباز در انتهای موضوع قرار میگیرد.",
    "sender": "فرستنده نامه",
    "receiver": "گیرنده نامه",
    "description": "توضیحات اضافی درباره نامه",
    "attachment_count": "تعداد فایل‌های پیوست شده",
    "main_image": "آپلود تصویر اصلی کارت",
    "normal_image": "آپلود تصویر جانبی/نرمال کارت",
}


CLEARANCE_LETTER_SAMPLE = [
    {
        'soldier_code': '0012345678',
        'reason': 'پایان خدمت',
        'letter_number': 'CL-5678-14031201',
        'absence_start_date': '1403/12/01',
        'absence_end_date': '1403/12/10',
        'description': 'توضیح نمونه ۱',
        'status': 'ایجاد شده',
    },
    {
        'soldier_code': '0098765432',
        'reason': 'انتقال',
        'letter_number': 'CL-4321-14031205',
        'absence_start_date': '1403/12/05',
        'absence_end_date': '1403/12/15',
        'description': 'توضیح نمونه ۲',
        'status': 'تأیید نهایی',
    }
]