from models import Script,ScriptArgs
from rest_framework import serializers
class ScriptSerializer(serializers.HyperlinkedModelSerializer):
    author_name=serializers.StringRelatedField(source="author.username",read_only=True)
    status=serializers.ChoiceField
    class Meta:
        model = Script
        fields = ('id', 'name', 'info','author_name','status'
                )

class ScriptArgsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScriptArgs
        fields= ('id','args_name','args_value')
