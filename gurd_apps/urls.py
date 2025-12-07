from django.urls import path
from .views import *

app_name = 'guards'

urlpatterns = [
    path('', guard_dashboard, name='dashboard'),
    path('/corrections', guard_corrections, name='corrections'),

]