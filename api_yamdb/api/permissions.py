# -*- coding: utf-8 -*-

from rest_framework import permissions

from users.managers import ADMIN, MODERATOR


class Admin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == ADMIN or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and (
                request.user.role == ADMIN or request.user.is_superuser
            )
        )

    def has_object_permission(self, request, view, obj):
        return(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and (
                request.user.role == ADMIN or request.user.is_superuser
            )
        )


class AdminOrModerOrAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        return(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return(
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.role == ADMIN
            or request.user.role == MODERATOR
            or request.user == obj.author
        )
