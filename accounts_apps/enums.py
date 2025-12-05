from enum import Enum
from typing import Optional

class AccountingRole(Enum):
    PASDAR = (0, "پاسدار")

    # نیرو انسانی (100–199)
    NIRU_ENSAN_FARMANDE = (100, "فرمانده نیروی انسانی")
    NIRU_ENSAN_KARGOZINI_VAZIFE = (101, "فرمانده کارگزینی وظیفه")
    NIRU_ENSAN_KARGOZINI_VAZIFE_SARBAZ = (102, "سرباز کارگزینی وظیفه")
    NIRU_ENSAN_KARGOZINI_RASMI = (103, "فرمانده کارگزینی رسمی")
    NIRU_ENSAN_GHADAEI = (104, "فرمانده قضایی")

    # قرارگاه (200–299)
    GHARARGAH_FARMANDE = (200, "فرمانده گردان قرارگاه")
    GHARARGAH_FIZIKI = (201, "فرمانده فیزیکی")
    GHARARGAH_SARBAZ_FIZIKI = (202, "سرباز حفاظت فیزیکی")
    GHARARGAH_JANESHIN = (203, "جانشین فرمانده قرارگاه")
    GHARARGAH_DEZBANI = (204, "فرمانده دژبانی")

    # فرماندهی (300–399)
    FARMANDEHI_RAHBAR = (300, "فرماندهی کل")
    FARMANDEHI_OPERATION = (301, "مسئول عملیات")
    FARMANDEHI_ETELAAT = (302, "مسئول اطلاعات")
    FARMANDEHI_HEIAT = (303, "رئیس هیئت")

    # آموزش (400–499)
    AMOOZESH_FARMANDE = (400, "فرمانده آموزش")
    AMOOZESH_MODARRES = (401, "مدرس دوره")
    AMOOZESH_BARNAME = (402, "مسئول برنامه‌ریزی آموزشی")

    # بهداری (500–599)
    BEHDARI_FARMANDE = (500, "فرمانده بهداری")
    BEHDARI_PEZECHK = (501, "پزشک یگان")
    BEHDARI_PARASTAR = (502, "پرستار")

    # آماد (600–699)
    AMAD_FARMANDE = (600, "فرمانده آماد")
    AMAD_TAJHIZAT = (601, "مسئول تجهیزات")
    AMAD_MAVAD = (602, "مسئول مواد مصرفی")

    # ترابری (700–799)
    TERABARI_FARMANDE = (700, "فرمانده ترابری")
    TERABARI_RANANDE = (701, "راننده")
    TERABARI_PARKBAN = (702, "مسئول پارکینگ خودروها")

    @property
    def code(self):
        return self.value[0]

    @property
    def label(self):
        return self.value[1]

    @classmethod
    def get_label(cls, key: int) -> Optional[str]:
        """
        دریافت label بر اساس کد عددی
        """
        for role in cls:
            if role.code == key:
                return role.label
        return None
        
# تبدیل برای Django
ROLE_CHOICES = [(role.code, role.label) for role in AccountingRole]
