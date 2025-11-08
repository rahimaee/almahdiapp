from django.urls import path
from .views import *

urlpatterns = [
    path("", ExpiredSoldierListView.as_view(), name="expired_soldiers"),
    path('search/', api_expired_soldiers_search, name='api_expired_soldiers_search'),
    path('import/group', expired_soldiers_import_group, name='expired_soldiers_import_group'),
    path('import/group/tasks/active', expired_soldiers_task_active, name='expired_soldiers_task_active'),
    path('import/group/action', expired_soldiers_import_group_action, name='expired_soldiers_import_group_action'),
    path('import/group/upload', expired_soldiers_import_group_upload, name='expired_soldiers_import_group_upload'),
    path('import/group/proccess', expired_soldiers_import_group_process_uploaded, name='expired_soldiers_import_group_process_uploaded'),
    path('import/group/database', expired_soldiers_manage_database, name='expired_soldiers_manage_database'),
    path('import/group/sample/expired-soldiers.xlsx', expired_soldiers_import_group_sample_excel, name='expired_soldiers_import_group_sample_excel'),
]