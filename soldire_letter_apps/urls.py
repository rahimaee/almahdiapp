from django.urls import path
from .views import *


urlpatterns = [
    path('clearance_letter_create/', ClearanceLetterCreateView.as_view(), name='clearance_letter_create'),
    path('ClearanceLetterListView/', ClearanceLetterListView.as_view(), name='ClearanceLetterListView'),
    path('clearance_letter/approved/<int:letter_id>/', approved_ClearanceLetter, name='approved_ClearanceLetter'),
    path('clearance_letter/print/<int:letter_id>/', print_ClearanceLetter, name='print_ClearanceLetter'),
    path('clearance_letter/excel', print_ClearanceLetter, name='clearance_letter_excel'),
    path('clearance_letter/delete/<int:letter_id>/', delete_ClearanceLetter, name='delete_ClearanceLetter'),
    path('clearance_letter/import/data', import_clearanceLetter_from_excel, name='import_clearanceLetter_from_excel'),
    path('clearance_letter/import/sample', import_clearanceLetter_sample_excel, name='import_clearanceLetter_sample_excel'),
    
    path('normal-letters/', normal_letter_list, name='normal_letter_list'),
    path('mental-health/retest/<int:test_id>/', create_new_letter_from_old, name='create_new_letter_from_old'),
    path('mental-health/retest/batch/', create_group_mental_health_letters,
         name='create_group_mental_health_letters'),
    path('judicial/', judicial_inquiry_list, name='judicial_inquiry_list'),
    path('judicial/create/', judicial_inquiry_create, name='judicial_inquiry_create'),
    path('judicial/edit/<int:pk>/', judicial_inquiry_edit, name='judicial_inquiry_edit'),
    path('judicial/delete/<int:pk>/', judicial_inquiry_delete, name='judicial_inquiry_delete'),
    path('judicial/print/<int:pk>/', judicial_inquiry_print, name='judicial_inquiry_print'),
    path('domestic_settlement/', domestic_settlement_list, name='domestic_settlement_list'),
    path('domestic_settlement/create/', domestic_settlement_create, name='domestic_settlement_create'),
    path('domestic_settlement/delete/<int:pk>/', domestic_settlement_delete, name='domestic_settlement_delete'),
    path('domestic_settlement/approved/<int:letter_id>/', approved_domestic_settlement,
         name='approved_domestic_settlement'),
    path('domestic_settlement/print/<int:letter_id>/', print_domestic_settlement, name='print_domestic_settlement'),
    path('introduction/', introduction_letter_list, name='introduction_letter_list'),
    path('introduction/create/', introduction_letter_create, name='introduction_letter_create'),
    path('introduction/<int:pk>/update/', introduction_letter_update, name='introduction_letter_update'),
    path('introduction/<int:pk>/delete/', introduction_letter_delete, name='introduction_letter_delete'),
    path('introduction/approved/<int:letter_id>/', approved_introduction_letter,
         name='approved_introduction_letter'),
    path('introduction/print/<int:letter_id>/', print_introduction_letter, name='print_introduction_letter'),
    path('ajax/load-sub-units/', load_sub_units, name='ajax_load_sub_units'),
    path('certificates/', membership_certificate_list, name='membership_certificate_list'),
    path('certificates/create/', membership_certificate_create, name='membership_certificate_create'),
    path('certificates/<int:pk>/edit/', membership_certificate_edit, name='membership_certificate_edit'),
    path('certificates/<int:pk>/delete/', membership_certificate_delete, name='membership_certificate_delete'),
    path('certificates/<int:pk>/print/', membership_certificate_print, name='membership_certificate_print'),
    path('health_iodine_letter/', health_iodine_letter_list, name='health_iodine_letter_list'),
    path('health_iodine_letter/create/', health_iodine_letter_create, name='health_iodine_letter_create'),
    path('health_iodine_letter/<int:pk>/update/', health_iodine_letter_update, name='health_iodine_letter_update'),
    path('health_iodine_letter/<int:pk>/delete/', health_iodine_letter_delete, name='health_iodine_letter_delete'),
    path('health_iodine_letter/print/<int:letter_id>/', print_health_iodine, name='print_health_iodine'),
    path('commitment_letter/', commitment_letter_list, name='commitment_letter_list'),
    path('commitment_letter/create/', commitment_letter_create, name='commitment_letter_create'),
    path('commitment_letter/<int:pk>/update/', commitment_letter_update, name='commitment_letter_update'),
    path('commitment_letter/<int:pk>/delete/', commitment_letter_delete, name='commitment_letter_delete'),
    path('commitment_letter/<int:pk>/print/', commitment_letter_print, name='print_commitment_letter'),
    path('letters/index', main_letters, name='main_letters'),
    
    # forms segment  
    path('forms/essential/list/',                 forms_essential_list, name='forms_essential_list'),
    path('forms/essential/<str:form_id>/remove/',  form_essential_delete, name='forms_essential_delete'),
    path('forms/essential/<str:form_type>/create/', form_essential_form, name='form_essential_create'),
    path('forms/essential/<str:form_type>/edit/<str:form_id>/', form_essential_form, name='form_essential_edit'),
    path('forms/essential/<str:form_id>/view/', form_essential_view, name='form_essential_view'),

    
]

urlpatterns = urlpatterns + [
    path('ready_forms/', ReadyFormsListView.as_view(), name='ready_forms'),
    path('ready_forms/create/', ReadyFormsCreateView.as_view(), name='ready_forms_create'),
    path('ready_forms/update/<int:pk>/', ReadyFormsUpdateView.as_view(), name='ready_formsupdate'),
    path('ready_forms/delete/<int:pk>/', ReadyFormsDeleteView.as_view(), name='ready_forms_delete'),
    path("runaway/", runaway_page, name="runaway_page"),
    path("runaway/<int:pk>/print", runaway_print_page, name="runaway_print_page"),
     # تغییر وضعیت نامه فرار
    path("runaway/<int:pk>/delete/", runaway_delete, name="runaway_delete"),
    path(
        'runaway/<int:pk>/change-status/<str:status>/',
        runaway_change_status,
        name='runaway_change_status'
    ),
]