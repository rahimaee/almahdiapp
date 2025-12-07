from django.urls import path
from .views import *

app_name = 'pasdar'

urlpatterns = [
    path('', pasdar_dashboard, name='dashboard'),

]
