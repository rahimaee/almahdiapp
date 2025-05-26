from soldires_apps.models import Soldier


def get_accessible_soldiers_for_user(user):
    if not user.is_authenticated:
        return Soldier.objects.none()  # بدون دسترسی

    accessible_units = user.units.all()
    if not accessible_units.exists():
        return Soldier.objects.none()

    soldiers = Soldier.objects.filter(current_parent_unit__in=accessible_units).all()
    return soldiers
