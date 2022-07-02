# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='api/redoc.html'),
        name='api_redoc'
    ),
    path('api/', include('api.urls', namespace='api')),
]