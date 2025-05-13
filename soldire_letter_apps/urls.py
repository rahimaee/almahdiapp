from django.urls import path
from .views import ClearanceLetterCreateView,ClearanceLetterListView

urlpatterns = [
    path('clearance_letter_create/', ClearanceLetterCreateView.as_view(), name='clearance_letter_create'),
    path('ClearanceLetterListView/', ClearanceLetterListView.as_view(), name='ClearanceLetterListView'),
]
