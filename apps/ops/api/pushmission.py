# -*- coding:utf-8 -*-
from .. import models
from .. import serializers
from rest_framework.views import Response,status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from ..permission import pushmission as PushMissionPermission
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination

__all__ = [
    'OpsPushMissionCreateAPI',
]


class OpsPushMissionCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.Push_Mission
    serializer_class = serializers.PushMissionSerializer
    # permission_classes = [PushMissionPermission.PushMissionCreateRequiredMixin]
    permission_classes = [AllowAny, ]
