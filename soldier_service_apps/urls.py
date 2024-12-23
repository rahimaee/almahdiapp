from django.urls import path
from . import views

urlpatterns = [
    path('soldier/<int:soldier_id>/edit/', views.SoldierServiceUpdateView.as_view(), name='soldier_service_edit'),
]

