# views.py
from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import ManagerPermission, Permission, AccessHistory, MyUser, Feature
from .forms import UserAccessForm, MyUserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# لیست مسئولین
def manager_list(request):
    managers = User.objects.all()  # استفاده از مدل User برای مسئولین
    return render(request, 'accounts_apps/manager_list.html', {'managers': managers})


# نمایش دسترسی‌های یک مسئول
def manager_permissions(request, manager_id):
    manager = get_object_or_404(User, id=manager_id)
    permissions = ManagerPermission.objects.filter(manager=manager)
    return render(request, 'accounts_apps/manager_permissions.html', {'manager': manager, 'permissions': permissions})


def manage_user_access(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)

    if request.method == "POST":
        form = UserAccessForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('panel_home')  # یا صفحه دلخواهت
    else:
        form = UserAccessForm(instance=user)

    return render(request, 'accounts_apps/manage_user_access.html', {'form': form, 'user_obj': user})


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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import MyUserForm

User = get_user_model()


def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts_apps/user_list.html', {'users': users})


def user_create(request):
    if request.method == 'POST':
        form = MyUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # فعلا ذخیره نکن، فقط شی بساز
            national_code = form.cleaned_data.get('id_code')  # فرض گرفتم کد ملی تو فرم هست
            if national_code:
                user.set_password(national_code)  # رمز رو با کد ملی ست کن
            else:
                user.set_password('1234')  # اگر احیانا کد ملی نبود، یه رمز پیش‌فرض بده
            user.save()  # حالا ذخیره کن
            messages.success(request, 'کاربر جدید با موفقیت اضافه شد.')
            return redirect('user_list')
    else:
        form = MyUserForm()
    return render(request, 'accounts_apps/user_form.html', {'form': form})


def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = MyUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات کاربر با موفقیت به‌روز شد.')
            return redirect('user_list')
    else:
        form = MyUserForm(instance=user)
    return render(request, 'accounts_apps/user_form.html', {'form': form})


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'کاربر با موفقیت حذف شد.')
        return redirect('user_list')
    return render(request, 'accounts_apps/user_confirm_delete.html', {'user': user})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # رمز عوض شد، لاگین بمونه
            messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد.')
            return redirect('profile')  # میتونی بری مثلا صفحه پروفایل یا هرجا خواستی
        else:
            messages.error(request, 'لطفاً خطاهای فرم را اصلاح کنید.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts_apps/change_password.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = MyUserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل با موفقیت بروزرسانی شد.')
            return redirect('profile')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید.')
    else:
        form = MyUserProfileForm(instance=request.user)

    # گرفتن اطلاعات گروه‌ها و پرمیشن‌ها
    user_groups = request.user.groups.all()
    user_permissions = request.user.user_permissions.all()
    is_admin = request.user.is_superuser  # اگر ادمین باشه
    user_units = request.user.units.all()
    user_features = request.user.features.all()

    return render(request, 'accounts_apps/profile.html', {
        'form': form,
        'user_groups': user_groups,
        'user_permissions': user_permissions,
        'is_admin': is_admin,
        'user_units': user_units,
        'user_features': user_features,
    })


@login_required
def profile_view(request):
    return render(request, 'accounts_apps/profile_card.html', {'user': request.user})


def import_feature(request):
    features = [
        'لیست سربازان',
        'اطلاعات کامل سرباز',
        'سرباز جدید',
        'ویرایش سرباز',
        'آپلود گروهی عکس بر اساس کد ملی',
        'تست مجدد روان پس از 6 ماه',
        'فراری ها',
        'ورودی های جدید',
        'نواقص پرونده',
        'بارگذاری عکس برای سرباز',
        'چاپ پرونده',
        'مدیریت مدارک سرباز',
        'کسریااضافه خدمت'
        'فرم مدیریت مرخصی',
    ]
    for name in features:
        Feature.objects.get_or_create(name=name)
    return HttpResponse("success")


def access_denied_view(request):
    reason = request.GET.get("reason")
    feature = request.GET.get("feature", "نامشخص")

    context = {
        "reason": reason,
        "feature": feature,
    }
    return render(request, "accounts_apps/access_denied.html", context)
