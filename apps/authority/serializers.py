import models
from rest_framework import serializers
from validate.models import ExtendUser
#__all__ = ['UserSerializer','AuthSerializer']
class UserSerializer(serializers.HyperlinkedModelSerializer):
    group_name = serializers.StringRelatedField(source="get_group_name",read_only=True)
    fullname = serializers.StringRelatedField(source="get_full_name",read_only=True)
    email = serializers.StringRelatedField(source="get_9531email",read_only=True)
    class Meta:
        model = ExtendUser
        fields = ('id','email', 'is_active', 'last_login','phone','username','fullname','group_name',
                )


class AuthSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        models = models.Group
        fields = ('id',)