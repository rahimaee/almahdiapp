from dataclasses import dataclass
import json
from typing import Any, Dict, Type

# فرم شماره 3
@dataclass
class ClearanceLetterFormData:
    shkh: str
    course_name: str
    course_number: int
    attachment_count: int = 1

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
    staff_name: str
    staff_id: str
    birth_year: int
    enlistment_date: str

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
