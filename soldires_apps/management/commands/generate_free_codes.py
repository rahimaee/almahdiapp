from django.core.management.base import BaseCommand
from soldires_apps.models import OrganizationalCode

class Command(BaseCommand):
    help = 'Generate OrganizationalCode entries from 1 to the specified max number'

    def add_arguments(self, parser):
        parser.add_argument(
            '--max',
            type=int,
            default=100,
            help='Maximum code number to generate (default 100)'
        )

    def handle(self, *args, **options):
        max_number = options['max']
        created_count = 0

        for number in range(1, max_number + 1):
            code, created = OrganizationalCode.objects.get_or_create(
                code_number=number,
                defaults={'is_active': False}  # حالت پیشفرض آزاد
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created OrganizationalCode {number}"))
            else:
                self.stdout.write(f"OrganizationalCode {number} already exists, skipped.")

        self.stdout.write(self.style.SUCCESS(f"Finished! {created_count} new codes created."))
