from django.urls import path
from . import views

urlpatterns = [
    path('naserin/', views.naserin_list, name='naserin_list'),
    path('naserin/sodlire/lsit/', views.soldire_naserin_list, name='soldire_naserin_list'),
    path('create/', views.naserin_create, name='naserin_create'),
    path('edit/<int:pk>/', views.naserin_edit, name='naserin_edit'),
    path('soldier/<int:soldier_id>/edit-naserin/', views.edit_soldier_naserin, name='edit_soldier_naserin'),
    path('soldiers/bulk-edit-naserin/', views.bulk_edit_naserin, name='bulk_edit_naserin'),
]
