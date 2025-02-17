from django.urls import path
from . import views

urlpatterns = [
    path('soldier/<int:soldier_id>/edit/', views.manage_soldier_vacation, name='soldier_vacation_edit'),
]

