# -*- coding: utf-8 -*-

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import yamdb_year_validator
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=80,
                            unique=True
                            )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название жанра')
    slug = models.SlugField(max_length=80,
                            unique=True
                            )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=255,
                            db_index=True,
                            verbose_name='Название произведения'
                            )
    year = models.IntegerField(validators=[yamdb_year_validator],
                               verbose_name='Год создания'
                               )
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='titles_of_category',
                                 verbose_name='Категория'
                                 )
    genre = models.ManyToManyField(Genre,
                                   related_name='titles_of_genre',
                                   verbose_name='Жанры'
                                   )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'year'],
                                    name='unique_title'
                                    )
        ]
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name}, {self.year}'


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведение'
                              )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Автор отзыва',
                               )
    text = models.TextField(verbose_name='Текст отзыва',
                            help_text='Введите текст отзыва'
                            )
    score = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1, 'Оценка не меньше 1!'),
            MaxValueValidator(10, 'Оценка не больше 10!'),
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации отзыва'
                                    )

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Отзыв'
                               )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор комментария',
                               )
    text = models.TextField(verbose_name='Текст комментария',
                            help_text='Введите текст комментария'
                            )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации'
                                    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
