# -*- coding:utf-8 -*-
from .models import Script,ScriptArgs
import serializers
from rest_framework.views import Response,status
from rest_framework import generics
from forms import ScriptForm
from rest_framework.permissions import IsAuthenticated
class ScriptListAPI(generics.ListAPIView):
    module = Script
    serializer_class = serializers.ScriptSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=Script.objects.all()
        return queryset

class ScriptArgsListAPI(generics.ListAPIView):
    module = ScriptArgs
    serializer_class = serializers.ScriptArgsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.kwargs['pk']=='0':
            queryset={}
            return queryset
        queryset = Script.objects.get(id=self.kwargs['pk']).scriptargs
        return queryset


class ScriptUpdateArgsAPI(generics.UpdateAPIView):
    module = Script
    serializer_class = serializers.ScriptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print('a')
        return
    def patch(self, request, *args, **kwargs):
        print('a')
        return