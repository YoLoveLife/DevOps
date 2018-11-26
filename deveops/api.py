# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-21
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework.views import Response, status
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

__all__ = [
    'WebTokenAuthentication'
]


class WebTokenAuthentication():
    authentication_classes = (JSONWebTokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    qrcode_response = Response({
        'detail': '您的QR-Code有误',
    }, status=status.HTTP_406_NOT_ACCEPTABLE)

    def qrcode_check(self, request):
        if 'qrcode' in request.data.keys() and request.user.check_qrcode(request.data.get('qrcode')):
            request.user.is_expire = request.data.get('qrcode')
            request.data.pop('qrcode')
            return True
        elif 'qrcode' not in request.data.keys() and not request.user.is_expire:
            return True
        else:
            return False
