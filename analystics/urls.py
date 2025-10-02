from django.urls import path
from . import views

app_name = "analystics"

urlpatterns = [
    path('', views.index, name='index'),
    path('latest_statistics', views.latest_statistics, name='latest_statistics'),
    path('reports/all', views.reports_all, name='reports_all'),
    path('reports/dagree', views.reports_dagree, name='reports_dagree'),
    path('reports/comprehensive', views.reports_comprehensive, name='reports_comprehensive'),
    path('reports/ages', views.reports_ages, name='reports_ages'),
    path('reports/percent', views.reports_percent, name='reports_percent'),
    path('reports/planning', views.reports_planning, name='reports_planning'),
    path('reports/near_end_service', views.reports_near_end_service, name='reports_near_end_service'),
    path('reports/skill_training', views.reports_skill_training, name='reports_skill_training'),
    path('reports/chip', views.reports_chip, name='reports_chip'),
    path('reports/type2', views.reports_type2, name='reports_type2'),
    path('reports/eshraf_create/', views.reports_eshraf_create, name='reports_eshraf_create'),
    path('reports/eshraf_zip/<int:eshraf_id>/', views.reports_eshraf_download_zip, name='reports_eshraf_download_zip'),
    path('reports/eshraf_delete/<int:eshraf_id>/', views.reports_eshraf_delete, name='reports_eshraf_delete'),
    path('reports/eshraf/', views.reports_eshraf, name='reports_eshraf'),
]
