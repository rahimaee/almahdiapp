from django.contrib import admin
from .models import Section, Permission, ManagerPermission, AccessHistory,Feature
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser


class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'description')
    search_fields = ('section_name',)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('permission_name', 'description')
    search_fields = ('permission_name',)


class ManagerPermissionAdmin(admin.ModelAdmin):
    list_display = ('manager', 'permission', 'granted_by')
    list_filter = ('granted_by', 'permission')
    search_fields = ('manager__username', 'permission__permission_name')


class AccessHistoryAdmin(admin.ModelAdmin):
    list_display = ('manager', 'permission', 'change_date', 'change_description')
    list_filter = ('manager', 'permission')
    search_fields = ('manager__username', 'permission__permission_name', 'change_description')


# ثبت مدل‌ها در پنل ادمین
admin.site.register(Section, SectionAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(ManagerPermission, ManagerPermissionAdmin)
admin.site.register(AccessHistory, AccessHistoryAdmin)
admin.site.register(Feature)



@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات', {'fields': (
        'first_name', 'last_name', 'email', 'national_code', 'phone_number', 'address', 'profile_picture', 'id_code',
        'Employment_status', 'units','role')}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌های مهم', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'national_code', 'email'),
        }),
    )
    list_display = ('username', 'email', 'national_code', 'is_staff')
    search_fields = ('username', 'email', 'national_code')
    ordering = ('username',)
