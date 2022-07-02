# -*- coding: utf-8 -*-

from django.urls import include, path
from rest_framework.routers import SimpleRouter
from users.urls import auth_urls

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

app_name = 'api'

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/users/', include('users.urls', namespace='users')),
    path('v1/', include(router.urls)),
]
