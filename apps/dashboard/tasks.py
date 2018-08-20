# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()

from celery.task import periodic_task
from django.conf import settings
from dashboard.models import ExpiredAliyunECS,ExpiredAliyunRDS,ExpiredAliyunKVStore,ExpiredAliyunMongoDB,DiskOverFlow


def obj_maker(MODELS, dict_models):
    MODELS.objects.create(**dict_models)


@periodic_task(run_every=settings.EXPIRED_TIME)
def expired_aliyun_ecs():
    ExpiredAliyunECS.objects.all().delete()
    from deveops.tools.aliyun import ecs
    API = ecs.AliyunECSTool()
    for page in range(1,API.pagecount+1):
        results = API.request_get_instances(page)
        for result in results:
            dict_models = API.get_aliyun_expired_models(result)
            if settings.ALIYUN_OVERDUETIME < dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
                obj_maker(ExpiredAliyunECS, dict_models)


@periodic_task(run_every=settings.EXPIRED_TIME)
def expired_aliyun_rds():
    ExpiredAliyunRDS.objects.all().delete()
    from deveops.tools.aliyun import rds
    API = rds.AliyunRDSTool()
    for page in range(1,API.pagecount+1):
        results = API.request_get_instances(page)
        for result in results:
            if not API.is_readonly(result):
                dict_models = API.get_aliyun_expired_models(result)
                if settings.ALIYUN_OVERDUETIME < dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
                    obj_maker(ExpiredAliyunRDS,dict_models)


@periodic_task(run_every=settings.EXPIRED_TIME)
def expired_aliyun_kvstore():
    ExpiredAliyunKVStore.objects.all().delete()
    from deveops.tools.aliyun import kvstore
    API = kvstore.AliyunKVStoreTool()
    for page in range(1,API.pagecount+1):
        results = API.request_get_instances(page)
        for result in results:
            dict_models = API.get_aliyun_expired_models(result)
            if settings.ALIYUN_OVERDUETIME < dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
                obj_maker(ExpiredAliyunKVStore,dict_models)


@periodic_task(run_every=settings.EXPIRED_TIME)
def expired_aliyun_mongodb():
    ExpiredAliyunMongoDB.objects.all().delete()
    from deveops.tools.aliyun import mongodb
    API = mongodb.AliyunMongoDBTool()
    for page in range(1,API.pagecount+1):
        results = API.request_get_instances(page)
        for result in results:
            dict_models = API.get_aliyun_expired_models(result )
            if settings.ALIYUN_OVERDUETIME < dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
                obj_maker(ExpiredAliyunMongoDB, dict_models)


from dashboard.ansible_v2.callback import DiskOverFlowCallback
from dashboard.ansible_v2.playbook import DiskOverFlowPlaybook

# @periodic_task(run_every=settings.DISK_TIME)
def disk_overflow():
    DiskOverFlow.objects.all().delete()
    from manager.models import Group,Host
    for group in Group.objects.all():
        if group.key is not None and group.jumper is not None:
            run_disk_overflow(group)
            break



import time, os, stat
def write_key(key, file_path):
    try:
        f = open(file_path, 'w')
        f.write(key.private_key)
        f.close()
    except Exception:
        return '~/.ssh/id_rsa'
    os.chmod(file_path, stat.S_IWUSR | stat.S_IRUSR)

    return file_path



def run_disk_overflow(group):
    # 准备变量
    vars_dict = {}

    for var in group.group_vars.all():
        vars_dict[var.key] = var.value

    if group.jumper is not None and group.key is not None:
        vars_dict['JUMPER_IP'] = group.jumper.connect_ip
        vars_dict['JUMPER_PORT'] = group.jumper.sshport

    # 创建临时目录
    TMP = settings.OPS_ROOT + '/' + str(time.time()) + '/'
    if not os.path.exists(TMP):
        os.makedirs(TMP)

    KEY = TMP + str(time.time()) + '.key'
    write_key(group.key, KEY)

    # Playbook实例
    callback = DiskOverFlowCallback()
    dof = DiskOverFlowPlaybook(group, KEY, callback)
    dof.import_vars(vars_dict)
    from dashboard.ansible_v2.play_source import PLAY_SOURCE

    PLAY_SOURCE[0]['hosts'] = list(group.hosts.filter(_status=settings.STATUS_HOST_CAN_BE_USE).values_list('connect_ip', flat=True))
    dof.import_task(PLAY_SOURCE)

    dof.run()

disk_overflow()