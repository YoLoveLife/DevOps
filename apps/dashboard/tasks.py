# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from celery.task import periodic_task
from django.conf import settings
from dashboard.models import ExpiredAliyunECS,ExpiredAliyunRDS,ExpiredAliyunKVStore,ExpiredAliyunMongoDB


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

