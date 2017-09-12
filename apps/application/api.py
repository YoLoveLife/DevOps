# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class DBListAPI(generics.ListAPIView):
    module = models.DB
    serializer_class = serializers.DBSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=models.DB.objects.all()
        return queryset