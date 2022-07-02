# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'slug',
                    )
    list_editable = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'slug',
                    )
    list_editable = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'year',
                    'category'
                    )
    list_editable = ('name', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('year', 'category', 'genre')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title_id', 'author', 'text', 'score', 'pub_date')
    list_editable = ('text',)
    search_fields = ('text',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'author', 'text', 'pub_date')
    list_filter = ('review_id', 'author')
    search_fields = ('text',)
    list_editable = ('text',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
