from django.contrib import admin
from soldires_apps.models import Soldier, OrganizationalCode, Settlement,PaymentReceipt

# Register your models here.

admin.site.register(Soldier)
admin.site.register(OrganizationalCode)
admin.site.register(Settlement)
admin.site.register(PaymentReceipt)
