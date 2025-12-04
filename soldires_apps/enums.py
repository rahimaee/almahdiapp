from enum import Enum

# ==========================
# تعریف فیلدهای کد سازمانی
# ==========================
class OrganizationalCodeEnum(Enum):
    NATIONAL_CODE = "national_code", "کد ملی"
    ORG_CODE = "org_code", "کد سازمانی"
    STATUS = "status", "وضعیت"

    @property
    def key(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]
    
# ==========================
# Enum برای تطبیق کد سازمانی با سرباز
# ==========================
class SoldierOrgCodeEnum(Enum):
    NATIONAL_CODE = "national_code", "کد ملی"
    ORG_CODE = "org_code", "کد سازمانی"
    NEW_STATUS = "new_status", "وضعیت جدید (اختیاری)"

    @property
    def key(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]
    
    
from enum import Enum

# ========================================================
# وضعیت مورد نظر (برای فرم بارگذاری اکسل)
# ========================================================
class OrganizationalCodeStatusEnum(Enum):
    INEXCEL     = "inexcel", "ستون وضعیت اکسل"
    ACTIVE      = "active", "فعال"
    INACTIVE    = "inactive", "غیرفعال"
    CHECKOUT    = "checkout", "تسویه حساب"
    FUGITIVE    = "FUGITIVE", "فراری"
    PRESENT     = "PRESENT", "حاظر"

    @property
    def key(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]


# ========================================================
# مدیریت کدهای موجود در سرور که در فایل اکسل نیستند
# ========================================================
class ExistingOrgCodeModeEnum(Enum):
    KEEP = "keep", "بدون تغییر"
    DEACTIVATE = "deactivate", "غیرفعال کردن کدهای موجود که در اکسل نیستند"
    ACTIVATE = "activate", "فعال کردن کدهای موجود که در اکسل نیستند"

    @property
    def key(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]


# ========================================================
# وضعیت مورد نظر در فرم تطبیق کد ملی با کد سازمانی سرباز
# ========================================================
class SoldierOrgCodeStatusEnum(Enum):
    NONE = "none", "بدون تغییر"
    INEXCEL = "inexcel", "ستون وضعیت اکسل"
    ACTIVE = "active", "فعال"
    INACTIVE = "inactive", "غیرفعال"
    CHECKOUT = "checkout", "تسویه حساب"

    @property
    def key(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]


# enums.py
from enum import Enum

class SoldierStatusFilterEnum(Enum):
    ALL = "", "همه سربازان"
    PRESENT_AND_ABSENT = "present_and_absent", "سربازان حاضر و فراری"
    PRESENT = "present", "سربازان حاضر"
    ABSENT = "absent", "سربازان فراری"
    CHECKOUT = "CHECKOUT", "تسویه حساب شده"

    @property
    def key(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]