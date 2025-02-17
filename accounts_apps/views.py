# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import ManagerPermission, Permission, AccessHistory
from .forms import ManagerPermissionForm


# لیست مسئولین
def manager_list(request):
    managers = User.objects.all()  # استفاده از مدل User برای مسئولین
    return render(request, 'accounts_apps/manager_list.html', {'managers': managers})


# نمایش دسترسی‌های یک مسئول
def manager_permissions(request, manager_id):
    manager = get_object_or_404(User, id=manager_id)
    permissions = ManagerPermission.objects.filter(manager=manager)
    return render(request, 'accounts_apps/manager_permissions.html', {'manager': manager, 'permissions': permissions})


# اختصاص دسترسی به مدیران زیرمجموعه
def assign_permission(request, manager_id):
    manager = get_object_or_404(User, id=request.user.id)
    permissions = Permission.objects.filter(managerpermission__manager=manager).distinct()

    if request.method == 'POST':
        permission_id = request.POST.get('permission')
        granted_by = request.user  # مسئول فعلی از طریق login شناخته شده است
        permission = get_object_or_404(Permission, id=permission_id)

        # ایجاد رکورد دسترسی
        manager_permission = ManagerPermission(manager=manager, permission=permission, granted_by=granted_by)
        manager_permission.save()

        # ثبت تاریخچه تغییرات
        history = AccessHistory(manager=manager, permission=permission, change_description="دسترسی جدید داده شد.")
        history.save()

        return redirect('accounts_apps/manager_permissions', manager_id=manager_id)

    return render(request, 'accounts_apps/assign_permission.html', {'manager': manager, 'permissions': permissions})
