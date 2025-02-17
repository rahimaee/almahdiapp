# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.soldier_list, name='soldier_list'),
    path('<int:pk>/', views.soldier_detail, name='soldier_detail'),
    path('<int:pk>/edit/', views.soldier_edit, name='soldier_edit'),
    path('create/', views.soldier_create, name='soldier_create'),
]
