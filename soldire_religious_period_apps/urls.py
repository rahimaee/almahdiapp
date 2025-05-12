from django.urls import path
from . import views

urlpatterns = [
    path('religious-period/', views.religious_period_list, name='religious_period_list'),
    path('add/', views.create_religious_period, name='religious_period_add'),
    path('<int:pk>/edit/', views.update_religious_period, name='religious_period_edit'),
    path('soldiers/without-training/', views.soldiers_without_ideological_training, name='soldiers_without_training'),
    path('soldiers/with-training/', views.soldiers_with_religious_period, name='soldiers_with_training'),
    path('soldier/<int:soldier_id>/edit-ideological/', views.edit_ideological_period, name='edit_ideological_period'),
    path('upload-excel/', views.upload_excel_view, name='upload-excel'),

]
