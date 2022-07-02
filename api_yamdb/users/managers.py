# -*- coding: utf-8 -*-

from django.contrib.auth.base_user import BaseUserManager

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
USER_ROLES = [
    (USER, 'Common User'),
    (MODERATOR, 'Moderator'),
    (ADMIN, 'Administrator'),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        if not email:
            raise ValueError('The e-mail must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('role', ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)
