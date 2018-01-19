# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response,status
from rest_framework.pagination import PageNumberPagination
from timeline.decorator.manager import decorator_manager

class UtilsJumperListAPI(generics.ListAPIView):
    module = models.Jumper
    serializer_class = serializers.JumperSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = models.Jumper.objects.all()
        return queryset