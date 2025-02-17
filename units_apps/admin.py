from django.contrib import admin
from .models import SubUnit, ParentUnit, UnitHistory

# Register your models here.

admin.site.register(SubUnit)
admin.site.register(ParentUnit)
admin.site.register(UnitHistory)
