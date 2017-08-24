import models
from rest_framework import serializers
class ScriptSerializer(serializers.HyperlinkedModelSerializer):
    author_name=serializers.StringRelatedField(source="author.username",read_only=True)
    status=serializers.ChoiceField
    class Meta:
        model = models.Script
        fields = ('id', 'name', 'info','author_name','status'
                )

class ScriptArgsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ScriptArgs
        fields= ('id','args_name','args_value')
