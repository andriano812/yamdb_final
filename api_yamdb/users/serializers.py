# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import User
from .utils import email_is_valid

USER_404 = 'NO_SUCH_USER'


class EmailAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    confirmation_code = serializers.CharField(max_length=100)

    def validate_username(self, data):
        if not User.objects.filter(username=data).exists():
            raise serializers.ValidationError(USER_404)
        return data

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if not User.objects.filter(username=username,
                                   confirmation_code=confirmation_code
                                   ).exists():
            raise serializers.ValidationError('Confirmation code is not valid')
        return data


class EmailCodeSerializer(serializers.Serializer):

    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        bad_data = {}
        if (not username
                or username == 'me'
                or User.objects.filter(username=username).exists()):
            bad_data['username'] = ['not_valid']
        if (not email_is_valid(email)
                or User.objects.filter(email=email).exists()):
            bad_data['email'] = ['not_valid']
        if bad_data:
            raise serializers.ValidationError(bad_data)
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'role', 'email')
        model = User
