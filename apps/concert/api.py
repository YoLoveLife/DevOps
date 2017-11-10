# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
__all__ = ['MusicListAPI']
class MusicListAPI(generics.ListAPIView):
    module = models.Music
    serializer_class = serializers.MusicSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=models.Music.objects.all()
        return queryset