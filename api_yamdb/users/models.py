# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import USER, USER_ROLES, CustomUserManager


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='адрес e-mail')
    role = models.CharField(
        max_length=9,
        choices=USER_ROLES,
        default=USER,
        verbose_name='Пользовательская роль'
    )
    bio = models.TextField(
        default='',
        verbose_name='Рассказ о себе'
    )
    confirmation_code = models.CharField(max_length=100, blank=True, )

    REQUIRED_FIELDS = ['email', 'role']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
