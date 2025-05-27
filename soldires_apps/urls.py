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
    path('mental-health/due/', views.due_mental_health_letters, name='due_mental_health_letters'),
    path('soldiers-by-entry-date/', views.soldiers_by_entry_date, name='soldiers_by_entry_date'),
    path('incomplete_soldiers_list/', views.incomplete_soldiers_list, name='incomplete_soldiers_list'),
    path('soldier/new/status/<int:pk>/letters/', views.soldires_new_status_view, name='soldires_new_status_view'),

]
