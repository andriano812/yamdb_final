# -*- coding: utf-8 -*-

from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        user = self.context['request'].user
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise serializers.ValidationError(
                'На это произведение уже оставлен отзыв'
            )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating',)
        model = Title


class TitleMakeSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
