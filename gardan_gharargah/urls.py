from django.urls import path
from .views import *

app_name= 'gardan'

urlpatterns = [
    path('dashboard', gardan_gharargah_dashboard, name='dashboard'),
    path('gurd/dashboard', gurd_dashboard, name='gurd_dashboard'),
]

