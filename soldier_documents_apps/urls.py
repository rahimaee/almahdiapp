from django.urls import path
from . import views

urlpatterns = [
    path('soldiers/<int:soldier_id>/documents/', views.manage_soldier_documents, name='manage_soldier_documents'),
]
