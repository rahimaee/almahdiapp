from django.urls import path
from . import views

urlpatterns = [
    path('parent-units/', views.parent_unit_list, name='parent_unit_list'),
    path('parent-units/new/', views.parent_unit_form, name='parent_unit_create'),
    path('parent-units/<int:pk>/edit/', views.parent_unit_form, name='parent_unit_edit'),
    path('parent-units/<int:pk>/delete/', views.parent_unit_delete, name='parent_unit_delete'),
    path('sub-units/', views.sub_unit_list, name='sub_unit_list'),
    path('sub-units/create/', views.sub_unit_form, name='sub_unit_create'),
    path('sub-units/edit/<int:pk>/', views.sub_unit_form, name='sub_unit_edit'),
    path('sub-units/delete/<int:pk>/', views.sub_unit_delete, name='sub_unit_delete'),
]
