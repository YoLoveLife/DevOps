# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response,status
from models import Group
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
#__all__ = ['UserListAPI','UserRemoveAPI']

class LoginJSONWebToken(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginJSONWebToken,self).post(request,*args,**kwargs)
        return response

class UserInfoJSONWebToken(generics.ListAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    def get(self, request, *args, **kwargs):
        dist = {}
        dist['username'] = request.user.username
        dist['name'] = request.user.last_name
        if request.user.is_oper == True or request.user.is_superuser == True:
            dist['isadmin'] = True
        elif request.user.is_oper == False and request.user.is_superuser == False:
            dist['isadmin'] = False
        else:
            dist['isadmin'] = 'None'

        return Response(dist, status=status.HTTP_201_CREATED)


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

class AuthListAPI(generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.AuthSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset =  models.Group.objects.all()
        return queryset

class PermissionListAPI(generics.ListAPIView):
    module = models.Permission
    serializer_class = serializers.PermissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.Permission.objects.all()
        return queryset

class PermissionUpdateAPI(generics.UpdateAPIView):
    module = Group
    serializer_class = serializers.GroupPermissionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):

        return Response({'info': '转换成功'}, status=status.HTTP_201_CREATED)