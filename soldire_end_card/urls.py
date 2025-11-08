from django.urls import path
from . import views

urlpatterns = [
    path('soldiers/soldiers_ready_for_card/', views.soldiers_ready_for_card, name='soldiers_ready_for_card'),
    path('card-series/', views.card_series_list, name='card_series_list'),
    path('card-series/create/', views.card_series_create, name='card_series_create'),
    path('card-series/<int:pk>/edit/', views.card_series_edit, name='card_series_edit'),
    path('card-send/list/', views.card_send_list_n, name='card_send_list_n'),
    path('card-send/<int:series_id>/list/', views.card_send_list_series, name='card_send_list_series'),
    path('card-send/<int:pk>/review/', views.review_card_send, name='review_card_send'),
    path('cards/', views.card_send_list, name='card_send_list'),
    path('cards/create/', views.card_send_create, name='card_send_create'),
    path('cards/<int:pk>/edit/', views.card_send_update, name='card_send_update'),
    path('cards/create/soldier/<int:soldier_id>/', views.card_send_create_for_soldier,
         name='card_send_create_for_soldier'),
    path("series/<int:series_id>/<str:status>/", views.change_series_status, name="change_series_status"),
    path("export_series/<int:series_id>/nzsa", views.export_series_nzsa, name="export_series_nzsa"),
]
