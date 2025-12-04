from django.utils import timezone
from soldires_apps.models import Soldier, Settlement
from .base import StatBase

# =====================
# پایه‌ای ترین دسته‌ها
# =====================

class AllSoldiers(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset


class PresentSoldiers(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False, is_fugitive=False)

    def get_queryset(self):
        return self.queryset


class RunawaySoldiers(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False, is_fugitive=True)

    def get_queryset(self):
        return self.queryset.filter(is_checked_out=False, is_fugitive=True)


class FinishedService(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        today = timezone.now().date()
        return self.queryset.filter(service_end_date__lte=today)


class PresentOutedService(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False, is_fugitive=False)

    def get_queryset(self):
        today = timezone.now().date()
        return self.queryset.filter(service_end_date__lt=today)


class CardIssuing(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset.filter(
            eligible_for_card_issuance=True,
            card_issuance_status__isnull=True
        )


class DebtCount(StatBase):
    base_queryset = Settlement.objects.filter(current_debt_rial__gt=0)

    def get_queryset(self):
        return self.queryset


class AbsorptionSoldiers(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset.filter(absorption=True)


class SystemPresenceNotReported(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset.filter(system_presence=False)


class NotReportedSoldiers(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset.filter(service_entry_date__isnull=True)


# =====================
# وضعیت سلامت
# =====================

class HealthySoldiers(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False, is_fugitive=False)

    def get_queryset(self):
        return self.queryset.filter(health_status="سالم")


class ExemptSoldiers(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False, is_fugitive=False)

    def get_queryset(self):
        return self.queryset.filter(health_status="معاف از رزم")


class ExemptBSoldiers(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False, is_fugitive=False)

    def get_queryset(self):
        safe_values = [
            'گروه ب',
            'معاف از رزم + گروه ب',
            'معاف از رزم+گروه ب',
        ]
        return self.queryset.filter(health_status__in=safe_values)

# =====================
# وضعیت تحصیلی
# =====================

class EducationDiploma(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset.filter(degree="دیپلم")


class EducationAssociate(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset.filter(degree="فوق دیپلم")


class EducationBachelor(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset.filter(degree="لیسانس")


class EducationMaster(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset.filter(degree="فوق لیسانس")


class EducationDoctor(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset.filter(degree="دکتری")


# =====================
# سایر آمار دلخواه
# =====================

class NeedClearanceSoldiers(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        today = timezone.now().date()
        return self.queryset.filter(service_end_date__lt=today)


class MonthlyEntrySoldiers(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        today = timezone.now().date()
        month_start = today.replace(day=1)
        return self.queryset.filter(service_entry_date__gte=month_start)


# =====================
# وضعیت تاهل
# =====================

class MarriedSoldiers(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset.filter(marital_status="متاهل")


class SingleSoldiers(StatBase):
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset.filter(marital_status="مجرد")


class EducationGroup(StatBase):
    """برگرداندن تعداد سربازان بر اساس مدرک به صورت دیکشنری"""
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset

    def get_grouped_counts(self):
        qs = self.get_queryset()
        result = {}

        # degree_choices از مدل Soldier خوانده می‌شود
        for degree, _ in Soldier._meta.get_field("degree").choices:
            result[degree] = qs.filter(degree=degree).count()

        return result


class RankGroup(StatBase):
    """برگرداندن تعداد سربازان بر اساس درجه به صورت دیکشنری"""
    base_queryset = Soldier.objects.filter(is_checked_out=False)

    def get_queryset(self):
        return self.queryset

    def get_grouped_counts(self):
        qs = self.get_queryset()
        result = {}

        # rank_choices از مدل Soldier خوانده می‌شود
        for rank, _ in Soldier._meta.get_field("rank").choices:
            result[rank] = qs.filter(rank=rank).count()

        return result


    def dagrees_grouped(self):
        qs = self.get_queryset()
        ranks = []
        for rank,_ in Soldier._meta.get_field("rank").choices:
            ranks.append(rank)
    
        soldiers = qs.filter(rank__in=ranks[0:3])
        dagrees = qs.filter(rank__in=ranks[4:8])
        officers = qs.filter(rank__in=ranks[9:11])
        soldiers_counts = soldiers.count()  
        dagrees_counts = dagrees.count()  
        officers_counts = officers.count()  
        totals = soldiers_counts + dagrees_counts + officers_counts
        
        return {
            'soldiers':soldiers,
            'dagrees':dagrees,
            'officers':officers,
            'soldiers_counts':soldiers_counts,
            'dagrees_counts':dagrees_counts,
            'officers_counts':officers_counts,
            'totals':totals,
        }
    def dagrees_grouped_counts(self):
        ret  = self.dagrees_grouped()
        print(ret)
        return {
            'soldiers':0,
            'dagrees':0,
            'officers':0,
            'total':0,
        }


class ActiveServiceStats(StatBase):
    """
    استعداد حاضر به خدمت (ستاد، عده، گردان، جمع و ...)
    """
    base_queryset = PresentSoldiers().get_queryset()
    
    def get_queryset(self):
        return self.queryset

    def get_data(self):
        qs = self.get_queryset()

        def group(rank_min, rank_max):
            group_qs = qs.filter(rank__gte=rank_min, rank__lte=rank_max)

            staff =     0      # ستاد
            unit =      0        # عده
            battalion = 0  # گردان
            total = staff + unit + battalion

            locals_count = group_qs.count()      # بومی
            nonlocals_count = 0                     # غیر بومی

            return {
                "staff": staff,
                "unit": unit,
                "battalion": battalion,
                "total": total,
                "py": total,
                "local": locals_count,
                "non_local": nonlocals_count,
            }

        return {
            "normal": group(1, 4),
            "daghree": group(5, 9),
            "officer": group(10, 12),
        }


class EducationExemptRunawayStats(StatBase):
    """
    قبولی دانشگاه / معافیت / فراری / انتقالی
    """
    base_queryset = AllSoldiers().get_queryset()

    def get_queryset(self):
        return self.queryset

    def get_data(self):
        qs = self.get_queryset()

        def group(rank_min, rank_max):
            group_qs = qs.filter(rank__gte=rank_min, rank__lte=rank_max)

            education = 0
            medical_exempt = 0
            non_medical_exempt = 0
            fugitive = group_qs.filter(is_fugitive=True).count()
            transferred = 0

            total = (education + medical_exempt + non_medical_exempt +
                     fugitive + transferred)

            return {
                "education": education,
                "medical_exempt": medical_exempt,
                "non_medical_exempt": non_medical_exempt,
                "fugitive": fugitive,
                "transferred": transferred,
                "total": total,
            }

        return {
            "normal": group(1, 4),
            "daghree": group(5, 9),
            "officer": group(10, 12),
        }


class StaffRetentionStats(StatBase):
    """
    ترخیص ماه آینده / کارت صادر شده (شیفتی-اداری) / مجموع
    """
    base_queryset = PresentSoldiers().get_queryset()
    
    def get_queryset(self):
        return self.queryset

    def get_data(self):
        qs = self.get_queryset()

        def group(rank_min, rank_max):
            group_qs = qs.filter(rank__gte=rank_min, rank__lte=rank_max)

            next_month_discharge = 0
            card_shift = 0
            card_admin = 0
            total = card_shift + card_admin

            return {
                "next_discharge": next_month_discharge,
                "shift": card_shift,
                "admin": card_admin,
                "total": total,
            }

        return {
            "normal": group(1, 4),
            "daghree": group(5, 9),
            "officer": group(10, 12),
        }


class CommandActiveServiceStats(StatBase):
    """
    فرماندهی بدون فراری / فرماندهی با فراری / حوزه / حفا / جمع
    """
    base_queryset = PresentSoldiers().get_queryset()
    
    def get_queryset(self):
        return self.queryset

    def get_data(self):
        qs = self.get_queryset()

        def group(rank_min, rank_max):
            group_qs = qs.filter(rank__gte=rank_min, rank__lte=rank_max)

            no_fugitive = group_qs.filter(is_fugitive=False).count()
            with_fugitive = group_qs.count()
            hozeh = 0
            hafa = 0
            total = with_fugitive + hozeh + hafa

            return {
                "no_fugitive": no_fugitive,
                "with_fugitive": with_fugitive,
                "hozeh": hozeh,
                "hafa": hafa,
                "total": total,
            }

        return {
            "normal": group(1, 4),
            "daghree": group(5, 9),
            "officer": group(10, 12),
        }

    
class HealthStats(StatBase):
    """
    وضعیت جسمانی و روانی
    """
    base_queryset = PresentSoldiers().get_queryset()
    
    def get_queryset(self):
        return self.queryset

    def get_data(self):
        present = self.get_queryset()

        normal =  HealthySoldiers(present).get_queryset().count()
        exempt =  ExemptSoldiers(present).get_queryset().count()
        exemptb = ExemptBSoldiers(present).get_queryset().count()
        exempta =  normal + exempt
        exempt_medical = ExemptBSoldiers(present).count()

        return {
            "normal": normal,
            "exempt": exempt_medical,
            "total1": normal + exempt_medical,
            "exempta": exemptb,
            "exemptb": exempta,
            "total2": exempta + exemptb,
        }


class RankGroupStats(StatBase):
    """
    تعداد افسر / درجه‌دار / عادی
    """
    
    base_queryset = PresentSoldiers().get_queryset()
    
    def get_queryset(self):
        return self.queryset

    def get_data(self):
        qs = self.get_queryset()
        ranks = []
        for rank,_ in Soldier._meta.get_field("rank").choices:
            ranks.append(rank)
    
        soldiers = qs.filter(rank__in=ranks[0:3])
        dagrees = qs.filter(rank__in=ranks[4:8])
        officers = qs.filter(rank__in=ranks[9:11])
        normal_counts = soldiers.count()  
        daghree_counts = dagrees.count()  
        officers_counts = officers.count()  
        totals = normal_counts + daghree_counts + officers_counts
        
        return {
            "officers": officers_counts,
            "daghrees": daghree_counts,
            "soldiers": normal_counts,
            "total": totals,
        }


class ReligionStats(StatBase):
    """
    شیعه / سنی / جمع کل
    """
    
    base_queryset = PresentSoldiers().get_queryset()
    
    def get_queryset(self):
        return self.queryset

    def get_data(self):
        qs = self.get_queryset()

        no_sunni = qs.filter(is_sunni=False).count()
        sunni = qs.filter(is_sunni=True).count()

        return {
            "no_sunni": no_sunni,
            "sunni": sunni,
            "total": no_sunni + sunni,
        }


class OtherStats(StatBase):
    """
    آمار پاسدار وظیفه / معتاد
    """
    base_queryset = PresentSoldiers().get_queryset()
    
    def get_queryset(self):
        return self.queryset

    def get_data(self):
        qs = self.get_queryset()

        guard = qs.filter(is_guard_duty=True).count()
        addicted = qs.filter(addiction_record=True).count()

        return {
            "guard": guard,
            "addicted": addicted,
            "total": guard + addicted,
        }
