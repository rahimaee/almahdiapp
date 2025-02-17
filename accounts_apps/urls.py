# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('managers/', views.manager_list, name='manager_list'),
    path('managers/<int:manager_id>/permissions/', views.manager_permissions, name='manager_permissions'),
    path('managers/<int:manager_id>/assign_permission/', views.assign_permission, name='assign_permission'),
]
