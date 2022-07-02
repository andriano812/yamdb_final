# -*- coding: utf-8 -*-

from django.contrib.auth.tokens import default_token_generator
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .managers import USER
from .serializers import (USER_404, EmailAuthSerializer, EmailCodeSerializer,
                          UserSerializer)
from .utils import generate_mail
from api.permissions import Admin
from reviews.models import User


class ObtainToken(TokenObtainPairView):
    serializer_class = EmailAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            username_not_valid = serializer.errors.get('username')
            if username_not_valid and username_not_valid[0] == USER_404:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = User.objects.get(username=username,
                                confirmation_code=confirmation_code
                                )
        token = str(RefreshToken.for_user(user))
        return Response({'token': token}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (Admin, )
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', )

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        if self.request.method == 'PATCH':
            data = request.data.copy()
            if self.request.user.role == USER:
                data['role'] = USER
            serializer = self.get_serializer(
                self.request.user,
                data=data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_email_with_code(request):
    serializer = EmailCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    user = User(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    generate_mail(email, confirmation_code)
    user.confirmation_code = confirmation_code
    user.save()
    return Response(
        {'username': username, 'email': email},
        status=status.HTTP_200_OK
    )
