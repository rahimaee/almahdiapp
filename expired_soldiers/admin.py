from django.contrib import admin
from .models import ExpiredSoldier

@admin.register(ExpiredSoldier)
class ExpiredSoldierAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "national_code",
        "expired_file_number",
        "end_service_date",
    )
    search_fields = ("first_name","last_name", "national_code")
