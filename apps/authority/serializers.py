import models
from rest_framework import serializers
from authority.models import ExtendUser,Group,Permission
#__all__ = ['UserSerializer','AuthSerializer']
class UserSerializer(serializers.HyperlinkedModelSerializer):
    group_name = serializers.StringRelatedField(source="get_group_name",read_only=True)
    fullname = serializers.StringRelatedField(source="get_full_name",read_only=True)
    email = serializers.StringRelatedField(source="get_8531email",read_only=True)
    class Meta:
        model = ExtendUser
        fields = ('id','email', 'is_active', 'last_login','phone','username','fullname','group_name',
                )

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('name','codename')

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name')

class GroupPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id')