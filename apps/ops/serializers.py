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


class QuickGitMissionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=True)
    src_git = serializers.CharField(write_only=True, required=True)
    src_branch = serializers.CharField(write_only=True, required=True)
    src_path = serializers.CharField(write_only=True, required=True)
    dest_path = serializers.CharField(write_only=True, required=True)

    hosts = serializers.PrimaryKeyRelatedField(required=True, many=True, queryset=models.Host.objects.all(), allow_null=True)
    group = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all(), required=True)
    need_validate = serializers.BooleanField(default=False)

    class Meta:
        model = models.Mission
        fields = (
            'name', 'src_git', 'src_branch', 'src_path', 'dest_path', 'hosts', 'group', 'need_validate'
        )

    def create(self, validated_data):
        # Checkout
        checkout_content = models.META_CONTENT.objects.create(
            name='检出代码Checkout',
            module='git',
            args='repo={SRC} dest={{BASE}}/code version={BRANCH}'.format(
                SRC=validated_data['src_git'],
                BRANCH=validated_data['src_branch'],
            ),
        )

        contents_list = models.META_CONTENT.objects.filter(id=checkout_content.id, uuid=checkout_content.uuid)

        checkout_meta = models.META.objects.create(
            group = validated_data['group'],
            info = validated_data['name']+'检出代码Checkout',
        )
        checkout_meta.contents.add(*contents_list)


        # Sync
        sync_content = models.META_CONTENT.objects.create(
            name='同步代码Sync',
            module='synchronize',
            args='src={{BASE}}/code{SRC} dest={DEST} compress=yes use_ssh_args=yes'.format(
                SRC=validated_data['src_path'],
                DEST=validated_data['dest_path'],
            ),
        )
        contents_list = models.META_CONTENT.objects.filter(id=sync_content.id, uuid=sync_content.uuid)

        sync_meta = models.META.objects.create(
            group = validated_data['group'],
            info = validated_data['name']+'同步代码Sync',
        )
        sync_meta.contents.add(*contents_list)
        sync_meta.hosts.set(validated_data['hosts'])


        mission = models.Mission.objects.create(
            group = validated_data['group'],
            info = validated_data['name'],
            need_validate = validated_data['need_validate'],
        )
        mission.metas.set([checkout_meta,sync_meta,])
        return mission


class QuickFileMissionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=True)
    filename = serializers.CharField(write_only=True, required=True)
    dest_file = serializers.CharField(write_only=True, required=True)

    hosts = serializers.PrimaryKeyRelatedField(required=True, many=True, queryset=models.Host.objects.all(), allow_null=True)
    group = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all(), required=True)
    need_validate = serializers.BooleanField(default=False)

    class Meta:
        model = models.Mission
        fields = (
            'name', 'filename', 'dest_file', 'hosts', 'group', 'need_validate'
        )

    def create(self, validated_data):
        # Copy
        copy_content = models.META_CONTENT.objects.create(
            name='拷贝文件Copy',
            module='copy',
            args='src=file:{{{{FILENAME}}}} dest={DEST}'.format(
                FILENAME=validated_data['filename'],
                DEST=validated_data['dest_file'],
            ),
        )
        contents_list = models.META_CONTENT.objects.filter(id=copy_content.id, uuid=copy_content.uuid)

        copy_meta = models.META.objects.create(
            group=validated_data['group'],
            info=validated_data['name'] + '拷贝文件Copy',
        )
        copy_meta.contents.add(*contents_list)
        copy_meta.hosts.set(validated_data['hosts'])

        mission = models.Mission.objects.create(
            group=validated_data['group'],
            info=validated_data['name'],
            need_validate=validated_data['need_validate'],
        )
        mission.metas.set([copy_meta, ])
        return mission


class QuickSerializer(serializers.Serializer):
    metatype = serializers.CharField(required=True,)
    data = serializers.JSONField(required=True,)

    class Meta:
        model = models.Quick
        fields = (
            'id', 'uuid', 'data', 'metatype'
        )

    #:TODO Maybe create wrong?
    def create(self, validated_data):
        data = validated_data.pop('data')
        if validated_data['metatype'] == 'git':
            ser = QuickGitMissionSerializer(data=data)
            if ser.is_valid():
                ser.save()
        elif validated_data['metatype'] == 'file':
            ser = QuickFileMissionSerializer(data=data)
            if ser.is_valid():
                ser.save()
        else:
            pass
        validated_data['data'] = data['name']
        validated_data['user'] = self.context['request'].user

        obj = models.Quick.objects.create(**validated_data)
        return obj
