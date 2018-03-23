import models
from rest_framework import serializers
from authority.models import ExtendUser,Group,Permission
#__all__ = ['UserSerializer','AuthSerializer']

# class GroupSerializer(serializers.ModelSerializer):


class UserSerializer(serializers.ModelSerializer):
    group_name = serializers.StringRelatedField(source="get_group_name",read_only=True)
    email8531 = serializers.StringRelatedField(source="get_8531email",read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True,queryset=models.Group.objects.all())
    class Meta:
        model = ExtendUser
        fields = ('id', 'is_active', 'last_login', 'phone', 'username', 'full_name', 'group_name', 'email8531','groups'
                )

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True,queryset=models.Permission.objects.all())
    class Meta:
        model = Group
        fields = ('id','name', 'permissions')

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id','name',)#'codename'
#
# class AuthSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('id','name')
#
# class GroupPermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('id')