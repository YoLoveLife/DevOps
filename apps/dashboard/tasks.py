# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
import redis
from django.utils import timezone as datetime
from celery.task import periodic_task
from celery.schedules import crontab
from django.conf import settings
from manager.models import Group, Host
from zdb.models import Instance
from ops.models import Push_Mission
from utils.models import FILE
from yodns.models import DNS
from authority.models import ExtendUser


# def obj_maker(MODELS, dict_models):
#     MODELS.objects.create(**dict_models)
#
#
# @periodic_task(run_every=settings.EXPIRED_TIME)
# def expired_aliyun_ecs():
#     ExpiredAliyunECS.objects.all().delete()
#     from deveops.tools.aliyun_v2.request import ecs
#     API = ecs.AliyunECSTool()
#     for dict_models in API.tool_get_instances_expired_models():
#         print(dict_models)
#         if settings.ALIYUN_OVERDUETIME < dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
#             obj_maker(ExpiredAliyunECS, dict_models)
#
#
# @periodic_task(run_every=settings.EXPIRED_TIME)
# def expired_aliyun_rds():
#     ExpiredAliyunRDS.objects.all().delete()
#     from deveops.tools.aliyun_v2.request import rds
#     API = rds.AliyunRDSTool()
#     for dict_models in API.tool_get_instances_expired_models():
#         if not dict_models['readonly']:
#             if settings.ALIYUN_OVERDUETIME < dict_models.get('expired') < settings.ALIYUN_EXPIREDTIME:
#                 obj_maker(ExpiredAliyunRDS, dict_models)
#
#
# @periodic_task(run_every=settings.EXPIRED_TIME)
# def expired_aliyun_kvstore():
#     ExpiredAliyunKVStore.objects.all().delete()
#     from deveops.tools.aliyun_v2.request import kvstore
#     API = kvstore.AliyunKVStoreTool()
#     for dict_models in API.tool_get_instances_expired_models():
#         if settings.ALIYUN_OVERDUETIME < dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
#             obj_maker(ExpiredAliyunKVStore, dict_models)
#
#
# @periodic_task(run_every=settings.EXPIRED_TIME)
# def expired_aliyun_mongodb():
#     ExpiredAliyunMongoDB.objects.all().delete()
#     from deveops.tools.aliyun_v2.request import mongodb
#     API = mongodb.AliyunMongoDBTool()
#     for dict_models in API.tool_get_instances_expired_models():
#         if settings.ALIYUN_OVERDUETIME < dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
#             obj_maker(ExpiredAliyunMongoDB, dict_models)


connect = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_SPACE,
    password=settings.REDIS_PASSWD,
)


@periodic_task(run_every=settings.DASHBOARD_STATS_COUNT)
def statistics_count():
    connect.delete('COUNT')
    count_dist = dict()
    count_dist['GROUP_COUNT'] = Group.objects.count()
    count_dist['HOST_COUNT'] = Host.objects.count()
    count_dist['DNS_COUNT'] = DNS.objects.count()
    count_dist['FILE_COUNT'] = FILE.objects.count()
    count_dist['USER_COUNT'] = ExtendUser.objects.count()
    count_dist['DBINSTANCE_COUNT'] = Instance.objects.count()

    for key, value in count_dist.items():
        connect.hset('COUNT', key, value)


week_list = ['Won', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']


@periodic_task(run_every=settings.DASHBOARD_STATS_WORK)
def statistics_work():
    connect.delete('WORK')
    work_dist = dict()
    import django
    now = django.utils.timezone.now().date()
    for i in range(6, -1, -1):
        start_day = now - datetime.timedelta(days=i)
        end_day = now - datetime.timedelta(days=i-1)
        weekday = start_day.weekday()
        work_dist[week_list[int(weekday)]] = Push_Mission.objects.filter(
            create_time__gt=start_day, create_time__lt=end_day
        ).count()
    for key, value in work_dist.items():
        connect.hset('WORK', key, value)


@periodic_task(run_every=settings.DASHBOARD_STATS_GROUP)
def statistics_group():
    connect.delete('GROUP')
    group_dist = {}
    for group in Group.objects.all():
        group_dist[group.name] = group.hosts.count()

    k = sorted(group_dist.items(), key=lambda x: x[1], reverse=True)
    count = 0
    for item in k:
        if count > 5:
            break
        connect.hset('GROUP', item[0], item[1])
        count = count+1
