# -*- coding:utf-8 -*-
import models,serializers
import models
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class UserListAPI(generics.ListAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=models.ExtendUser.objects.all()
        return queryset