# permissions_middleware.py
from django.contrib.auth.models import Permission

class PermObject:
    """
    شیء برای دسترسی به پرمیشن‌ها به صورت flat.
    حتی اگر attribute وجود نداشته باشد، False برمی‌گرداند.
    مثال: request.perm.pasdar_can_view
    """
    def __init__(self):
        self._store = {}

    def __getattr__(self, item):
        # اگر موجود نبود، False برگردان
        return self._store.get(item, False)

    def set(self, key, value=True):
        self._store[key] = value


class LoadUserPermissionsMiddleware:
    """
    Middleware که همه پرمیشن‌های کاربر را به صورت flat
    در request.perm قرار می‌دهد.
    مثال: request.perm.can_view_pasdar
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.perm = PermObject()
        user = getattr(request, 'user', None)

        if user and user.is_authenticated:
            # پرمیشن‌های مستقیم کاربر
            all_permissions = list(user.user_permissions.all())
            # پرمیشن‌های گروه‌ها
            all_permissions += list(Permission.objects.filter(group__user=user))

        for perm in all_permissions:
            key = f"can_{perm.codename}"
            request.perm.set(key, True)

        response = self.get_response(request)
        return response
