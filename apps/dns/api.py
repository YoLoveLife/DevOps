# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from timeline.decorator.manager import decorator_manager
from deveops.api import WebTokenAuthentication


class ManagerGroupListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.DNS
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Group.objects.all()