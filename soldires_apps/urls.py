# urls.py
from django.urls import path,include
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
    path('settlement/payments/<int:settlement_id>/', views.settlement_payments_view, name='settlement_payments'),
    path('mental-health/due/', views.due_mental_health_letters, name='due_mental_health_letters'),
    path('soldiers-by-entry-date/', views.soldiers_by_entry_date, name='soldiers_by_entry_date'),
    path('incomplete_soldiers_list/', views.incomplete_soldiers_list, name='incomplete_soldiers_list'),
    path('checked_out_soldiers_list/', views.checked_out_soldiers_list, name='checked_out_soldiers_list'),
    path('soldier/new/status/<int:pk>/letters/', views.soldires_new_status_view, name='soldires_new_status_view'),
    # ORGANIZATIONAL CODES
    path('organizational-codes/', views.organizational_codes_list, name='organizational_codes_list'),
    path('organizational-codes/match', views.organizational_code_match_view, name='organizational_codes_match'),
    path('organizational-codes/match/sample/organizational_code_soldier', 
         views.organizational_code_match_soldier_org_code_sample, 
         name='organizational_code_match_soldier_org_code_sample'
    ),
    path('organizational-codes/match/sample/organizational_code', 
         views.organizational_code_match_org_code_sample, 
         name='organizational_code_match_org_code_sample'
    ),
    
    path('organizational-codes/match/organizational_code', 
         views.organizational_code_match_org_code, 
         name='organizational_code_match_org_code'
    ),
    
    path('organizational-codes/crud', views.organizational_codes_list,   name='organizational_codes_crud'),
    path('organizational-codes/doc', views.organizational_codes_list,    name='organizational_codes_doc'),
    # GROUP SUBMIT
    path('group-submit/download-template/', views.download_soldiers_template, name='download_soldiers_template'),
    path('group-submit/', views.soldiers_group_submit, name='soldiers_group_submit'),
    path('api/soldiers/search', views.soldiers_search, name='soldiers_search'),
    path('soldiers/<int:soldier_id>/reports/single/', views.single_reports_soldier, name='single_reports_soldier'),
    path('soldiers/date_to_end/', views.soldiers_date_to_end, name='soldiers_date_to_end'),
    path('position/', include('organizational_position.urls')),
]
