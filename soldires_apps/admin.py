from django.contrib import admin
from django.utils.html import format_html
from .models import Soldier
from django.db.models import Case, When, Value, BooleanField, F,Func
from django.db import models
from django.utils.translation import gettext_lazy as _

@admin.register(Soldier)
class SoldierAdmin(admin.ModelAdmin):

    list_display = ["id", "first_name", "last_name", "national_code", "organizational_code", "is_active_org_code", "rank", "current_parent_unit", "current_sub_unit", "marital_status", "blood_group", "service_end_date_display", "health_status", "is_checked_out"]
    list_filter = ["rank", "marital_status", "health_status", "blood_group", "traffic_status", "is_guard_duty", "is_fugitive", "is_needy", "is_sayyed", "is_sunni", "absorption", "status", "is_checked_out", "current_parent_unit", "current_sub_unit", "degree", "skill_group", "skill_certificate", "independent_married", "eligible_for_card_issuance"]
    search_fields = ["first_name", "last_name", "national_code", "id_card_code", "father_name", "phone_mobile", "postal_code", "card_chip", "expired_file_number", "saman_username"]
    readonly_fields = ["remaining_days", "remaining_str", "remaining_str_type", "clearance_expired_file_number", "organizational_code_display", "is_active_org_code"]
    ordering = []

    fieldsets = [
        ("مشخصات فردی", {"fields": ["organizational_code", "organizational_code_display", "is_active_org_code", "first_name", "last_name", "national_code", "father_name", "id_card_code", "birth_date", "birth_place", "issuance_place", "marital_status", "number_of_children", "status", "is_checked_out"]}),
        ("سلامت", {"fields": ["health_status", "health_status_description", "blood_group", "naserin_group"]}),
        ("سکونت و اطلاعات تماس", {"fields": ["residence_city", "residence_province", "postal_code", "phone_home", "phone_mobile", "phone_virtual", "phone_parents", "address"]}),
        ("نظامی", {"fields": ["rank", "is_guard_duty", "is_fugitive", "fugitive_record", "addiction_record", "referral_person", "dispatch_date", "training_duration", "basic_training_center", "service_duration_completed", "service_entry_date", "essential_service_duration", "service_end_date", "total_service_adjustment", "service_deduction_type", "service_extension_type", "remaining_days", "remaining_str", "remaining_str_type", "current_parent_unit", "current_sub_unit", "traffic_status"]}),
        ("گواهینامه", {"fields": ["has_driving_license", "driving_license_type"]}),
        ("مدارک و مهارت‌ها", {"fields": ["degree", "field_of_study", "skill_5", "skill_group", "skill_certificate", "number_of_certificates", "is_certificate"]}),
        ("سایر", {"fields": ["saman_username", "card_chip", "ideological_training_period", "independent_married", "weekly_or_monthly_presence", "is_needy", "expertise", "is_sunni", "is_sayyed", "photo_scan", "eligible_for_card_issuance", "card_issuance_status", "expired_file_number", "clearance_expired_file_number", "system_presence", "absorption", "Is_the_Basij_sufficient", "height", "weight", "eye_color", "hair_color", "position", "position_at", "file_shortage", "comments"]}),
    ]


    def is_active_org_code(self, obj):
            return obj.organizational_code and obj.organizational_code.current_soldier_id == obj.id
    is_active_org_code.boolean = True
    is_active_org_code.short_description = _("کد فعال")
    is_active_org_code.admin_order_field = "is_active"
    def service_end_date_display(self, obj):
        return  obj.service_end_date_display
    
    service_end_date_display.short_description = "تاریخ پایان خدمت"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            is_active=Case(
                When(organizational_code__current_soldier_id=F('id'), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
        )
        qs = qs.order_by('-is_active', 'organizational_code__code_number')
        return qs
    def military_status_badge(self, obj):
        colors = {"serving": "#007bff", "escaped": "#dc3545", "done": "#444", "exempt": "#28a745"}
        labels = {"serving": "در حال خدمت", "escaped": "فرار", "done": "اتمام", "exempt": "معاف"}
        color, label = colors.get(obj.military_status, "#6c757d"), labels.get(obj.military_status, "نامشخص")
        return format_html("<span style='background:{}; color:white; padding:4px 8px; border-radius:4px; font-size:12px; display:inline-block;'>{}</span>", color, label)
    military_status_badge.short_description = "وضعیت خدمت"

    def avatar_preview(self, obj):
        if not obj.photo_scan:
            return format_html("<span style='background:#bbb; color:#333; padding:3px 6px; border-radius:4px; font-size:11px;'>بدون عکس</span>")
        return format_html("<img src='{}' style='width:40px; height:40px; object-fit:cover; border-radius:6px;' />", obj.photo_scan.url)
    avatar_preview.short_description = "عکس"

    class Media:
        css = {"all": ("admin_rtl.css",)}
