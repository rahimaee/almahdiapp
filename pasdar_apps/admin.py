from django.contrib import admin
from .models import Pasdar

@admin.register(Pasdar)
class PasdarAdmin(admin.ModelAdmin):
    list_display = ('code', 'first_name', 'last_name', 'national_id', 'section', 'role_in_section', 'created_at')
    search_fields = ('code', 'first_name', 'last_name', 'national_id')
