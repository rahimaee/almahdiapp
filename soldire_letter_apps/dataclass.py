from dataclasses import dataclass
import json
from typing import Any, Dict,Optional
from .constants import *


# فرم شماره 3 - داده‌ها با مقدار پیش‌فرض
@dataclass
class ClearanceLetterFormData:
    # ---------------- اطلاعات پایه ----------------
    first_name: str = ""                      # نام
    last_name: str = ""                       # نام خانوادگی
    father_name: str = ""                     # نام پدر
    birth_certificate_number: str = "1"       # شماره شناسنامه
    national_code: str = ""                    # کد ملی
    rank: str = ""                             # درجه
    employee_type: str = "وظیفه"              # نوع کارمند (کادر، بسیجی، وظیفه) - radio
    unit_name: str = "اموزشگاه رزم مقدماتی المهدی (عج) بابل"  # محل خدمت
    deployment_area: str = "اداره کل وظیفه عمومی نیروی انتظامی"  # حوزه اعزام کننده
    discharge_unit: str = "اموزشگاه رزم مقدماتی المهدی (عج) بابل"  # یگان ترخیص‌کننده

    # ---------------- اطلاعات تکمیلی ----------------
    birth_date: str = ""                        # تاریخ تولد
    birth_place: str = ""                       # محل تولد
    card_issue_date: str = ""                   # تاریخ صدور کارت
    eye_color: str = ""                         # رنگ چشم
    blood_group: str = ""                        # گروه خون
    height: float = 0                            # قد
    service_branch: str = ""                     # رسته خدمتی
    education_level: str = ""                    # مدرک تحصیلی
    specialty_code: str = ""                     # کد تخصصی
    military_education_status: str = ""         # وضعیت آموزشی نظامی
    legal_service_duration: int = 21            # مدت قانونی خدمت (ماه)
    served_duration: int = 21                    # مدت خدمت انجام شده (ماه)
    service_start_date: str = ""                 # تاریخ شروع خدمت
    service_end_date: str = ""                   # تاریخ خاتمه خدمت
    personal_code: str = ""                      # شماره پرسنلی / کد پاسداری
    main_office_number: str = ""                 # شماره دفتر اساس
    detailed_office_number: str = ""             # شماره دفتر تفضیلی

    # ---------------- اطلاعات فرم ----------------
    card_type: str = "المثنی"                   # نوع کارت: المثنی، تعویضی، مفقودی - radio
    main_image: Optional[str] = None            # عکس اصلی کارت
    normal_image: Optional[str] = None          # عکس جانبی/نرمال کارت


# صدور کارت پایور
@dataclass
class OfficerCardFormData:
    officer_name: str
    officer_id: str
    rank: str
    enlistment_date: str

# صدور کارت سرباز
@dataclass
class SoldierCardFormData:
    soldier_name: str
    soldier_id: str
    unit: str
    enlistment_date: str

# فرم تسویه حساب 3 فرزندی و بالاتر
@dataclass
class Checkout3PlusFormData:
    soldier_name: str
    soldier_id: str
    children_count: int
    discharge_date: str

# فعال سازی اعزام کارکنان قدیمی
@dataclass
class ActivateOldStaffFormData:
    staff_name: str = ''
    staff_id: str = ''
    birth_year: int = 0
    enlistment_date: str = ''

# گواهی دو پاسدار
@dataclass
class CertificateTwoGuardFormData:
    soldier_name: str
    soldier_id: str
    first_guard_date: str
    second_guard_date: str

# معافیت دائم کارکنان وظیفه
@dataclass
class PermanentExemptionFormData:
    soldier_name: str
    soldier_id: str
    exemption_reason: str
    exemption_date: str


def form_data_to_json(form_type: str, data: Dict[str, Any]) -> str:
    """
    فرم را بر اساس form_type به کلاس مربوطه نگاشت کرده و JSON آن را برمی‌گرداند.
    
    :param form_type: یکی از کلیدهای FORM_CLASSES
    :param data: دیکشنری شامل داده‌های فرم
    :return: رشته JSON
    """
    cls = FORM_CLASSES.get(form_type)
    if not cls:
        raise ValueError(f"فرم با نوع '{form_type}' پشتیبانی نمی‌شود.")
    
    # ساخت نمونه کلاس با داده‌ها
    form_instance = cls(**data)
    
    # تبدیل به JSON
    return json.dumps(form_instance.__dict__, ensure_ascii=False, indent=2)
