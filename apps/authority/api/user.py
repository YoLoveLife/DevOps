# -*- coding:utf-8 -*-
import pyotp, os
from qrcode import QRCode,constants
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import Response,status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.views import ObtainJSONWebToken
from django.conf import settings
from deveops.api import WebTokenAuthentication
from authority.permission import user as UserPermission
from deveops.utils import aes
from timeline.decorator import decorator_api
from .. import models,serializers,filter


__all__ = [
    "UserLoginAPI", "UserInfoAPI", "UserListAPI",
    "UserOpsListAPI", "UserUpdateAPI", "UserDeleteAPI",
    "UserListByPageAPI", 'UserPagination', 'UserOpsListByPageAPI',
    'UserQRCodeAPI', 'UserCreateAPI',
]


class UserLoginAPI(ObtainJSONWebToken):
    msg = settings.LANGUAGE.UserLoginAPI

    @decorator_api(timeline_type = settings.TIMELINE_KEY_VALUE['None_LOGIN'])
    def post(self, request, *args, **kwargs):
        response = super(UserLoginAPI, self).post(request, *args, **kwargs)
        return self.msg.format(
            USERNAME = request.data['username']
        ), response

class UserInfoAPI(WebTokenAuthentication, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        dist = {}
        dist['username'] = request.user.username
        dist['name'] = request.user.full_name
        if request.user.is_superuser == True:
            dist['isadmin'] = True
        else:
            dist['isadmin'] = 'None'

        return Response(dist, status=status.HTTP_200_OK)


class UserPagination(PageNumberPagination):
    page_size = 10


class UserListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    queryset = models.ExtendUser.objects.all()
    permission_classes = [UserPermission.UserListRequiredMixin,IsAuthenticated]
    filter_class = filter.UserFilter


class UserListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    queryset = models.ExtendUser.objects.all()
    permission_classes = [UserPermission.UserListRequiredMixin,IsAuthenticated]
    pagination_class = UserPagination
    filter_class = filter.UserFilter


class UserOpsListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    queryset = models.ExtendUser.objects.filter(groups__name__contains='运维')
    permission_classes = [UserPermission.UserOpsListRequiredMixin, IsAuthenticated]


class UserOpsListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    queryset = models.ExtendUser.objects.filter(groups__name__contains='运维')
    permission_classes = [UserPermission.UserOpsListRequiredMixin, IsAuthenticated]
    pagination_class = UserPagination


class UserCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    queryset = models.ExtendUser.objects.all()
    permission_classes = [UserPermission.UserCreateRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.UserCreateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['ExtendUser_USER_CREATE'])
    def create(self, request, *args, **kwargs):
        response = super(UserCreateAPI, self).create(request, *args, **kwargs)
        return self.msg.format(
            USER = request.user.full_name,
            USERNAME = response.data['username'],
            FULLNAME = response.data['full_name'],
        ), response


class UserUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    queryset = models.ExtendUser.objects.all()
    permission_classes = [UserPermission.UserUpdateRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.UserUpdateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['ExtendUser_USER_UPDATE'])
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        response = super(UserUpdateAPI, self).update(request, *args, **kwargs)
        return self.msg.format(
            USER = request.user.full_name,
            USERNAME = user.username,
            FULLNAME = user.full_name,
        ), response


class UserDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.ExtendUser
    serializer_class = serializers.UserSerializer
    queryset = models.ExtendUser.objects.all()
    permission_classes = [UserPermission.UserDeleteRequiredMixin,IsAuthenticated]
    msg = settings.LANGUAGE.UserDeleteAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['ExtendUser_USER_DELETE'])
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        response = super(UserDeleteAPI, self).delete(request, *args, **kwargs)
        return self.msg.format(
            USER = request.user.full_name,
            USERNAME = user.username,
            FULLNAME = user.full_name,
        ), response


def get_qrcode(user):
    if not user.qrcode: # ''
        user.qrcode = pyotp.random_base32()
        user.save()
    file_name = str(aes.encrypt(user.qrcode),encoding='utf-8')
    file = settings.QCODE_ROOT+'/'+file_name+'.png'
    if not os.path.exists(file):
        data = pyotp.totp.TOTP(user.qrcode).provisioning_uri(user.username, issuer_name="devEops")
        print('data',data)
        qr = QRCode(
            version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=6,
            border=4,)
        try:
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image()
            img.save(file)
            return '/media/qrcode/'+ file_name +'.png'
        except Exception as e:
            return '/media/qrcode/'+ file_name +'.png'
    else:
        return '/media/qrcode/' + file_name + '.png'


class UserQRCodeAPI(WebTokenAuthentication, APIView):
    permission_classes = [IsAuthenticated,]
    msg = settings.LANGUAGE.UserQRCodeAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['ExtendUser_USER_QRCODE'])
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.have_qrcode is False:
            dist = {"url":get_qrcode(request.user)}
            user.have_qrcode = True
            user.save()
            response = Response(dist, status=status.HTTP_201_CREATED)
            return self.msg.format(
                USER = request.user.full_name,
            ), response
        else:
            return '', Response({'detail': '当前用户已经扫描过QRCode 如有需要请联系管理员'}, status=status.HTTP_406_NOT_ACCEPTABLE)