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
    path('review_settlements/', views.review_settlements, name='review_settlements'),
    path('payment_receipt_create/', views.payment_receipt_create, name='payment_receipt_create'),
    path('soldiers_settlement_list/', views.soldiers_settlement_list, name='soldiers_settlement_list'),
    path('settlement/<int:settlement_id>/payments/', views.settlement_payments_view, name='settlement_payments'),
]
