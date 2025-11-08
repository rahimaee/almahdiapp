from django.core.management.base import BaseCommand
from soldires_apps.models import Soldier

class Command(BaseCommand):
    help = 'Populate current_soldier field for all OrganizationalCode entries'

    def handle(self, *args, **kwargs):
        soldiers = Soldier.objects.all()
        total = soldiers.count()
        self.stdout.write(f"Found {total} soldiers. Updating current_soldier for each...")

        for idx, soldier in enumerate(soldiers, start=1):
            # قبل از save، کد و سرباز فعلی قبلی را بگیریم
            code = soldier.organizational_code
            previous_current = getattr(code, 'current_soldier', None) if code else None

            # save مدل اجرا می‌شود و current_soldier بروزرسانی می‌شود
            soldier.save()

            # لاگ
            if code:
                self.stdout.write(
                    f"[{idx}/{total}] Soldier {soldier.first_name} {soldier.last_name} "
                    f"(ID: {soldier.id}) updated for Code {code.code_number}. "
                    f"Previous current_soldier: "
                    f"{previous_current.first_name if previous_current else 'None'} -> "
                    f"New: {code.current_soldier.first_name if code.current_soldier else 'None'}"
                )
            else:
                self.stdout.write(
                    f"[{idx}/{total}] Soldier {soldier.first_name} {soldier.last_name} "
                    f"(ID: {soldier.id}) has no OrganizationalCode"
                )

        self.stdout.write(self.style.SUCCESS("All OrganizationalCode entries updated!"))
