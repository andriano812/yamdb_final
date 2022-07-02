# -*- coding: utf-8 -*-

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from .filters import TitleFilter
from .mixins import CreateRetrieveViewSet
from .permissions import AdminOrModerOrAuthor, IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleMakeSerializer, TitleSerializer)
from reviews.models import Category, Comment, Genre, Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = ReviewSerializer
    permission_classes = (AdminOrModerOrAuthor,)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        author = self.request.user
        serializer.save(author=author, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()


class GenreViewSet(CreateRetrieveViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(CreateRetrieveViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrModerOrAuthor,)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        author = self.request.user
        serializer.save(author=author, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleMakeSerializer
        return TitleSerializer
