# -*- coding: utf-8 -*-
from ops import models
from rest_framework import serializers

__all__ = [
    "MetaSerializer", "MetaContentSerializer", "MissionNeedFileSerializer",
    "MissionSerializer",
]

class MetaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.META_CONTENT
        fields = (
            'id', 'name', 'module', 'args', 'sort',
        )
        read_only_fields = (
            'id',
        )


class MetaSerializer(serializers.ModelSerializer):
    hosts = serializers.PrimaryKeyRelatedField(required=False,many=True, queryset=models.Host.objects.all(),allow_null=True)
    need_files = serializers.ListField(source="file_list", read_only=True)
    contents = MetaContentSerializer(required=True, many=True, allow_null=True)
    group = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all())
    group_name = serializers.CharField(source="group.name",read_only=True)
    qrcode = serializers.CharField(required=True, write_only=True,)

    class Meta:
        model = models.META
        fields = (
            'id', 'uuid', 'hosts', 'contents', 'group', 'group_name', 'info', 'qrcode', 'need_files'
        )
        read_only_fields = (
            'id', 'uuid','group_name'
        )

    def create(self, validated_data):
        contents = validated_data.pop('contents')
        validated_data.pop('qrcode')
        id_list = []
        hosts = None
        for content in contents:
            content_instance = models.META_CONTENT.objects.create(**content)
            id_list.append(content_instance.id)

        if 'hosts' in validated_data.keys():
            hosts = validated_data.pop('hosts')

        contests_list = models.META_CONTENT.objects.filter(id__in=id_list)

        obj = models.META.objects.create(**validated_data)
        obj.contents.add(*contests_list)
        if hosts is not None:
            obj.hosts.set(hosts)
        obj.save()

        return obj

    def update(self, instance, validated_data):
        contents = validated_data.pop('contents')
        validated_data.pop('qrcode')
        obj = super(MetaSerializer,self).update(instance,validated_data)
        for content in obj.contents.all():
            content.delete()
        obj.contents.clear()

        id_list = []
        for content in contents:
            content_instance = models.META_CONTENT.objects.create(**content)
            id_list.append(content_instance.id)

        contests_list = models.META_CONTENT.objects.filter(id__in=id_list)
        obj.contents.add(*contests_list)
        obj.save()
        return obj


class MissionNeedFileSerializer(serializers.ModelSerializer):
    filelist = serializers.ListField(source='file_list',read_only=True)

    class Meta:
        model = models.Mission
        fields = (
            'filelist',
        )


class MissionSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all())
    metas = serializers.PrimaryKeyRelatedField(many=True, queryset=models.META.objects.all())
    group_name = serializers.CharField(source="group.name",read_only=True)
    counts = serializers.IntegerField(source="count",read_only=True)

    class Meta:
        model = models.Mission
        fields = (
            'id', 'uuid', 'group', 'metas', 'info', 'need_validate', 'group_name', 'counts'
        )
        read_only_fields = (
            'id', 'uuid', 'group_name', 'counts'
        )


class QuickGitMeta(serializers.ModelSerializer):
    src_git = serializers.CharField(write_only=True, required=False)
    src_branch = serializers.CharField(write_only=True, required=False)
    src_path = serializers.CharField(write_only=True, required=False)
    dest_path = serializers.CharField(write_only=True, required=False)

    class Meta:
        models = models.META

    def create(self, validated_data):
        checkout_model = models.META_CONTENT.create(
            name='检出代码Checkout',
            module='git',
            args='repo={SRC} dest={{BASE}}/code version={BRANCH}'.format(
                SRC=validated_data['src_git'],
                BRANCH=validated_data['src_branch'],
            ),
            sort=1
        )
        sync_model = models.META_CONTENT.create(
            name='同步代码Sync',
            module='synchronize',
            args='src={{BASE}}/code{SRC} dest={DEST} compress=yes use_ssh_args=yes'.format(
                SRC=validated_data['src_path'],
                DEST=validated_data['dest_path'],
            ),
            sort=2
        )
        models.META



class QuickSerializer(serializers.ModelSerializer):
    gitmeta = QuickGitMeta(required=False, write_only=True)

    src_file = serializers.CharField(write_only=True, required=False)
    dest_file = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = models.Quick
        fields = (
            'id', 'uuid', 'src_git', 'src_file', 'src_path', 'dest_path',
        )

    def create(self, validated_data):
        if validated_data['src_git']:# 如果是git创建
            pass
        elif validated_data['src_file']:
            upload_modle = models.META_CONTENT.create(
                name = '上传文件Upload',
                module = 'copy',
                args = 'src=file:{{{FILE}}} dest={DEST}'.format(
                    FILE = validated_data['src_file'],
                    DEST = validated_data['dest_file'],
                )
            )