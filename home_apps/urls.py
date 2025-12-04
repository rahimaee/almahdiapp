from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='panel_home'),
    path('manages', views.manages_app, name='manages_app'),
    path('export/excels', views.export_soldiers_excel, name='export_soldiers'),
    path('support', views.support_page, name='support'),
]
