# -*- coding:utf-8 -*-
from .. import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import Response,status
from rest_framework_jwt.views import ObtainJSONWebToken
from deveops.api import WebTokenAuthentication
from authority.permission import user as UserPermission

__all__ = [
    "UserLoginAPI", "UserInfoAPI", "UserListAPI",
    "UserOpsListAPI", "UserUpdateAPI", "UserDeleteAPI"
]


class UserLoginAPI(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super(UserLoginAPI,self).post(request,*args,**kwargs)
        return response


class UserInfoAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.ExtendUser
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        dist = {}
        dist['username'] = request.user.username
        dist['name'] = request.user.full_name
        if request.user.is_superuser == True:
            dist['isadmin'] = True
        else:
            dist['isadmin'] = 'None'

        return Response(dist, status=status.HTTP_201_CREATED)


class UserListAPI(generics.ListAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    queryset = models.ExtendUser.objects.all()
    permission_classes = [UserPermission.UserListRequiredMixin,IsAuthenticated]


class UserOpsListAPI(generics.ListAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    queryset = models.ExtendUser.objects.filter(groups__name__contains='运维')
    permission_classes = [UserPermission.UserOpsListRequiredMixin,IsAuthenticated]


class UserUpdateAPI(generics.UpdateAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    queryset = models.ExtendUser.objects.all()
    permission_classes = [UserPermission.UserUpdateRequiredMixin,IsAuthenticated]


class UserDeleteAPI(generics.DestroyAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    queryset = models.ExtendUser.objects.all()
    permission_classes = [UserPermission.UserDeleteRequiredMixin,IsAuthenticated]
