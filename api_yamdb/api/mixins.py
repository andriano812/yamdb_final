# -*- coding: utf-8 -*-

from rest_framework import mixins, viewsets


class CreateRetrieveViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    pass
