from enum import Enum

class ClearanceLetterEnum(Enum):
    LETTER_NUMBER      = ("letterNumber", "نامه شماره")
    NATIONAL_CODE      = ("nationalCode", "کد ملی")
    FIRST_NAME         = ("firstName", "نام")
    LAST_NAME          = ("lastName", "نام خانوادگی")
    ISSUED_AT          = ("issuedAt", "تاریخ صدور تسویه کل")
    FINISHED_AT        = ("finishedAt", "تاریخ پایان خدمت")
    DEGREE             = ("degree", "درجه")
    EXPIRED_FILE       = ("expiredFileNumber", "شماره پرونده منقضی")
    DESCRIPTION        = ("description", "توضیحات")

    def __init__(self, key, label):
        self.key = key        # این نامی است که در مدل استفاده می‌شود
        self.label = label    # این نام ستون داخل اکسل است

    @classmethod
    def keys(cls):
        return [item.key for item in cls]

    @classmethod
    def labels(cls):
        return [item.label for item in cls]
    
    @classmethod
    def label_of(cls, key):
        for item in cls:
            if item.key == key:
                return item.label
        return None
    