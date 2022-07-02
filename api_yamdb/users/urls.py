# -*- coding: utf-8 -*-

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ObtainToken, UserViewSet, send_email_with_code

auth_urls = [
    path('signup/', send_email_with_code, name='confirmation_email'),
    path('token/',
         ObtainToken.as_view(),
         name='token_obtain_pair'),
]

router = SimpleRouter()
router.register('', UserViewSet)

app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
]
