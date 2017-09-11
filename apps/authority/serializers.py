import models
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    group_name = serializers.StringRelatedField(source="get_group_name",read_only=True)
    fullname = serializers.StringRelatedField(source="get_full_name",read_only=True)
    class Meta:
        model = models.ExtendUser
        fields = ('id','email', 'is_active', 'last_login','phone','username','fullname','group_name',
                )


