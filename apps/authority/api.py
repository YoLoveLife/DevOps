# -*- coding:utf-8 -*-
import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response,status
from models import Group
from rest_framework_jwt.views import ObtainJSONWebToken
from deveops.api import WebTokenAuthentication
#__all__ = ['UserListAPI','UserRemoveAPI']

class LoginJSONWebToken(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginJSONWebToken,self).post(request,*args,**kwargs)
        return response

class UserInfoJSONWebToken(WebTokenAuthentication,generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        dist = {}
        dist['username'] = request.user.username
        dist['name'] = request.user.full_name
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
    queryset = models.ExtendUser.objects.all()

class UserUpdateAPI(generics.UpdateAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.ExtendUser.objects.all()

class UserDeleteAPI(generics.DestroyAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    # permission_classes = [HostPermission.HostDeleteRequiredMixin]
    queryset = models.ExtendUser.objects.all()

class GroupListAPI(generics.ListAPIView):
    module = models.Group
    serializer_class =serializers.GroupSerializer
    queryset = models.Group.objects.all()

class GroupCreateAPI(generics.CreateAPIView):
    module = models.Group
    serializer_class =serializers.GroupSerializer
    permission_classes = [IsAuthenticated]

class GroupUpdateAPI(generics.UpdateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Group.objects.all()

class GroupDeleteAPI(generics.DestroyAPIView):
    module =models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Group.objects.all()

class PermissionListAPI(generics.ListAPIView):
    module = models.Permission
    serializer_class = serializers.PermissionSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Permission.objects.filter(codename__istartswith="yo_")


# class GroupListAPI(generics.ListAPIView):
#     module = models.Group
#     serializer_class =serializers.GroupSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = models.Group.objects.all()


# class UserRemoveAPI(WebTokenAuthentication,generics.DestroyAPIView):
#     module = models.ExtendUser
#     serializer_class = serializers.UserSerializer
#     permission_classes = [IsAuthenticated]
#
#     def delete(self, request, *args, **kwargs):
#         if models.ExtendUser.objects.filter(id=int(kwargs['pk'])).exists():
#             models.ExtendUser.objects.get(id=int(kwargs['pk'])).delete()
#             return Response({'info': '删除成功'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'info': '该用户不存在'}, status=status.HTTP_406_NOT_ACCEPTABLE)
#

# class AuthGrpListAPI(WebTokenAuthentication,generics.ListAPIView):
#     module = models.Group
#     serializer_class = serializers.AuthSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         queryset =  models.Group.objects.all()
#         return queryset
#
#
# class PermissionAddForGroup(WebTokenAuthentication,generics.UpdateAPIView):
#     module = models.Group
#     serializer_class = serializers