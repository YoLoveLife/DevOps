# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response,status

class UserListAPI(generics.ListAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset=models.ExtendUser.objects.all()
        return queryset

class UserRemoveAPI(generics.DestroyAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        if models.ExtendUser.objects.filter(id=int(kwargs['pk'])).exists():
            models.ExtendUser.objects.get(id=int(kwargs['pk'])).delete()
            return Response({'info': '删除成功'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'info': '该用户不存在'}, status=status.HTTP_406_NOT_ACCEPTABLE)

# class AuthListAPI(generics.ListAPIView):
#     module = models.Group
#     serializer_class = serializers.AuthSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         queryset =  models.Group.objects.all()
#         return queryset