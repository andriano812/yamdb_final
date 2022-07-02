# -*- coding: utf-8 -*-

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'username',
                    'role',
                    )
    list_editable = ('role',)
    search_fields = ('username', 'email')
    list_filter = ('username',)
    empty_value_display = '-пусто-'
