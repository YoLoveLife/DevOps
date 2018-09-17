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
from dashboard.models import ExpiredAliyunECS,ExpiredAliyunRDS,ExpiredAliyunKVStore,ExpiredAliyunMongoDB


def obj_maker(MODELS, dict_models):
    MODELS.objects.create(**dict_models)


@periodic_task(run_every=settings.EXPIRED_TIME)
def expired_aliyun_ecs():
    ExpiredAliyunECS.objects.all().delete()
    from deveops.tools.aliyun_v2.request import ecs
    API = ecs.AliyunECSTool()
    for dict_models in API.tool_get_instances_expired_models():
        print(dict_models)
        if settings.ALIYUN_OVERDUETIME < dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
            obj_maker(ExpiredAliyunECS, dict_models)


@periodic_task(run_every=settings.EXPIRED_TIME)
def expired_aliyun_rds():
    ExpiredAliyunRDS.objects.all().delete()
    from deveops.tools.aliyun_v2.request import rds
    API = rds.AliyunRDSTool()
    for dict_models in API.tool_get_instances_expired_models():
        if not dict_models['readonly']:
            if settings.ALIYUN_OVERDUETIME < dict_models.get('expired') < settings.ALIYUN_EXPIREDTIME:
                obj_maker(ExpiredAliyunRDS, dict_models)


@periodic_task(run_every=settings.EXPIRED_TIME)
def expired_aliyun_kvstore():
    ExpiredAliyunKVStore.objects.all().delete()
    from deveops.tools.aliyun_v2.request import kvstore
    API = kvstore.AliyunKVStoreTool()
    for dict_models in API.tool_get_instances_expired_models():
        if settings.ALIYUN_OVERDUETIME < dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
            obj_maker(ExpiredAliyunKVStore,dict_models)


@periodic_task(run_every=settings.EXPIRED_TIME)
def expired_aliyun_mongodb():
    ExpiredAliyunMongoDB.objects.all().delete()
    from deveops.tools.aliyun_v2.request import mongodb
    API = mongodb.AliyunMongoDBTool()
    for dict_models in API.tool_get_instances_expired_models():
        if settings.ALIYUN_OVERDUETIME < dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
            obj_maker(ExpiredAliyunMongoDB, dict_models)
