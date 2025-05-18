# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.escaped_soldiers_view, name='escaped_soldiers'),
    path('<int:soldier_id>/', views.soldier_escape_details, name='soldier_escape_details'),
]
