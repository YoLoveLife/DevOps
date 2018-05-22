# -*- coding:utf-8 -*-
from application import models,serializers
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from manager.permission import host as HostPermission
from deveops.api import WebTokenAuthentication

# class ExpiredPagination(PageNumberPagination):
#     page_size = 10
#
#
# class ApplicationExpiredAliyunRDSAPI(WebTokenAuthentication,generics.ListAPIView):
#     module = models.ExpiredAliyunRDS
#     serializer_class = serializers.ExpiredAliyunRDSSerializer
#     queryset = models.ExpiredAliyunRDS.objects.all().order_by('expired')
#     # permission_classes = [HostPermission.HostLihoststRequiredMixin,IsAuthenticated]
#     permission_classes = [AllowAny,]
#     pagination_class = ExpiredPagination
#     filter_fields = '__all__'
#
#



#__all__ = ['DBListAPI','DBAuthAPI','DBAuthCreateAPI','DBAuthRemoveAPI','DBRemoveAPI']
# class DBListAPI(generics.ListAPIView):
#     serializer_class = serializers.DBSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         queryset=models.DB.objects.all()
#         return queryset
#
# class DBRemoveAPI(generics.DestroyAPIView):
#     serializer_class = serializers.DBSerializer
#     permission_classes = [IsAuthenticated]
#
#     def delete(self, request, *args, **kwargs):
#         if models.DB.objects.filter(id=int(kwargs['pk'])).exists():
#             models.DB.objects.get(id=int(kwargs['pk'])).delete()
#             return Response({'info': '删除成功'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'info': '该数据库不存在'}, status=status.HTTP_406_NOT_ACCEPTABLE)
#
# class DBAuthAPI(generics.ListAPIView):
#     serializer_class = serializers.DBAuthSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         queryset = models.DB.objects.filter(id=self.kwargs['pk']).get().dbuser.all()
#         return queryset
#
# class DBAuthCreateAPI(generics.CreateAPIView):
#     serializer_class = serializers.DBAuthSerializer
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         db = models.DB.objects.get(id=int(kwargs['pk']))
#         serializer.instance.db = db
#         serializer.save()
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
# class DBAuthRemoveAPI(generics.DestroyAPIView):
#     serializer_class = serializers.DBAuthSerializer
#     permission_classes = [IsAuthenticated]
#
#     def delete(self, request, *args, **kwargs):
#         if models.DB.objects.get(id=int(kwargs['pk'])).dbuser.filter(user=request.data['user'],ip=request.data['ip']).exists():
#             models.DB.objects.get(id=int(kwargs['pk'])).dbuser.filter(user=request.data['user'], ip=request.data['ip']).delete()
#             return Response({'info': '删除成功'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'info': '该数据库用户不存在'}, status=status.HTTP_406_NOT_ACCEPTABLE)
#
#
# class RedisListAPI(generics.ListAPIView):
#     serializer_class = serializers.RedisSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         queryset = models.Redis.objects.all()
#         return queryset