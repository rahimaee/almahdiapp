# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.soldier_list, name='soldier_list'),
    path('<int:pk>/', views.soldier_detail, name='soldier_detail'),
    path('<int:pk>/edit/', views.soldier_edit, name='soldier_edit'),
    path('create/', views.soldier_create, name='soldier_create'),
    path('soldier/<int:soldier_id>/upload-photo/', views.upload_soldier_photo, name='upload_soldier_photo'),
    path('soldiers/bulk-upload-photo/', views.bulk_photo_upload, name='bulk_photo_upload'),
]
