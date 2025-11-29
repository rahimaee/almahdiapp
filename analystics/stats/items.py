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
        return self.queryset


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
