from application import models
from rest_framework import serializers
#__all__ = ['DBSerializer','DBAuthSerializer']



# class DBSerializer(serializers.HyperlinkedModelSerializer):
#     host_name = serializers.CharField(source='host.hostname',read_only=True)
#     connect_ip = serializers.CharField(source='host.connect_ip',read_only=True)
#     class Meta:
#         model = models.DB
#         fields = ('id','host_name','port','datadir','connect_ip',
#                 )
#
# class DBAuthSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = models.DBUser
#         fields = ('user','ip')
#
# class RedisSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = models.Redis
#         fields = ('id','url','port','online')