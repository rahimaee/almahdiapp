# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('managers/', views.manager_list, name='manager_list'),
    path('managers/<int:manager_id>/permissions/', views.manager_permissions, name='manager_permissions'),
    path('managers/<int:manager_id>/assign_permission/', views.assign_permission, name='assign_permission'),
    path('manage-user-access/<int:user_id>/', views.manage_user_access, name='manage_user_access'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('change-password/', views.change_password, name='change_password'),
    path('profile/', views.profile_view, name='profile'),
    path('import_feature/', views.import_feature, name='import_feature'),
    path('access-denied/', views.access_denied_view, name='access_denied'),
]
