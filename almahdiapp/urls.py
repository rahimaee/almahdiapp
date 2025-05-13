"""
URL configuration for almahdiapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from home_apps.views import *

urlpatterns = [
    path('', include('home_apps.urls')),
    path('admin/', admin.site.urls),
    path('soldiers/', include('soldires_apps.urls')),
    path('documents/', include('soldier_documents_apps.urls')),
    path('services/', include('soldier_service_apps.urls')),
    path('vacation/', include('soldier_vacation_apps.urls')),
    path('training/', include('training_center_apps.urls')),
    path('accounts/', include('accounts_apps.urls')),
    path('units/', include('units_apps.urls')),
    path('iran_c_p/', include('cities_iran_manager_apps.urls')),
    path('naserin/', include('soldire_naserin_apps.urls')),
    path('religious-period/', include('soldire_religious_period_apps.urls')),
    path('card/', include('soldire_end_card.urls')),
    path('letter/', include('soldire_letter_apps.urls')),
    re_path(r'^header_partial_view',
            header_partial_view,
            name='header_partial_view'),
    re_path(r'^header_references_partial_view',
            header_references_partial_view,
            name='header_references_partial_view'),
    re_path(r'^footer_partial_view',
            footer_partial_view,
            name='footer_partial_view'),
    re_path(r'^footer_references_partial_view',
            footer_references_partial_view,
            name='footer_references_partial_view'),
    re_path(r'^navbar_partial_view',
            navbar_partial_view,
            name='navbar_partial_view'),

]
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# add media static files
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
