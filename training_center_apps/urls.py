from django.urls import path
from . import views

urlpatterns = [
    path('', views.training_center_list, name='training_center_list'),
    path('create/', views.training_center_create, name='training_center_create'),
    path('<int:pk>/edit/', views.training_center_edit, name='training_center_edit'),
    path('<int:pk>/delete/', views.training_center_delete, name='training_center_delete'),
]
