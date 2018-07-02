# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab
from pyecharts import Pie
from deveops import settings
import redis, datetime, json, os
from ops import models as OpsModels
from authority import models as AuthModels
from dashboard.models import ExpiredAliyunECS,ExpiredAliyunRDS,ExpiredAliyunKVStore,ExpiredAliyunMongoDB
from tool import smtp

connect = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_SPACE,password=settings.REDIS_PASSWD)

@periodic_task(run_every=settings.DASHBOARD_TIME)
def weeklyDashboard():
    import jinja2
    loader = jinja2.FileSystemLoader(settings.BASE_DIR+'/apps/dashboard/docs/', encoding='utf-8')
    env = jinja2.Environment(loader=loader)
    template = env.get_template("week")
    print('123',connect.keys())
    status_json = connect.get('MANAGER_STATUS')
    manager_status = json.loads(str(status_json, encoding='utf-8'))
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    TMP = settings.DASHBOARD_ROOT + '/' + now
    if not os.path.exists(TMP):
        os.makedirs(TMP)

    dic = {'GROUP_COUNT': manager_status['group_count'],
           'HOST_COUNT': manager_status['host_count'],
           'ALIYUN_COUNT': manager_status['position'][0]['value'],
           'VMWARE_COUNT': manager_status['position'][1]['value'],
           'MISSION_COUNT': OpsModels.Mission.objects.count(),
           'ACTIVITY_USER': AuthModels.ExtendUser.objects.count(),
           'WEEK_START': (datetime.datetime.now() - datetime.timedelta(days = 7)).strftime("%Y年%m月%d日"),
           'WEEK_END': datetime.datetime.now().strftime('%Y年%m月%d日'),
           }

    systype = manager_status['systemtype']
    attr = []
    v1 = []
    for l in systype:
        attr.append(l["name"])
        v1.append(l["value"])
    pie = Pie("操作系统类型", title_pos='right', width=900)
    pie.add("操作系统类型", attr, v1, center=[50, 50], is_random=True, radius=[30, 75], is_legend_show=False, is_label_show=True)
    pie.render(path=TMP+'/systype.png')

    groups = manager_status['groups']
    attr = []
    v1 = []
    for l in groups:
        attr.append(l["name"])
        v1.append(l["value"])
    pie = Pie("接管应用与主机总数", title_pos='right', width=900)
    pie.add("接管应用与主机总数", attr, v1, center=[50, 50], is_random=True, radius=[30, 75], is_legend_show=False, is_label_show=True)
    pie.render(path=TMP+'/group.png')

    if ExpiredAliyunECS.objects.count() !=0:
        ecsquery = ExpiredAliyunECS.objects.all()
        dic['ECS_EXPIRED'] = ecsquery

    if ExpiredAliyunRDS.objects.count() !=0:
        rdsquery = ExpiredAliyunRDS.objects.all()
        dic['RDS_EXPIRED'] = rdsquery

    if ExpiredAliyunKVStore.objects.count() !=0:
        kvsquery = ExpiredAliyunKVStore.objects.all()
        dic['KVSTORE_EXPIRED'] = kvsquery

    if ExpiredAliyunMongoDB.objects.count() !=0:
        kvsquery = ExpiredAliyunMongoDB.objects.all()
        dic['MONGODB_EXPIRED'] = kvsquery

    markdown = template.render(dic)

    with open(TMP+'/index.md','w') as f:
        f.write(markdown)

    #    <link href="../static/github.css" rel="stylesheet">
    html = '''
        <html lang="zh-cn">
        <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type" />
        <link href="../static/screen.css" rel="stylesheet">
        </head>
        <body>
        %s
        </body>
        </html>
        '''

    import markdown2
    html = html%markdown2.markdown(markdown,extras=['tables','break-on-newline'])

    with open(TMP+'/index.html','w') as f:
        f.write(html)

    msg = '本周平台周报地址http://deveops.8531.cn:8888/media/dashboard/'+ datetime.datetime.now().strftime('%Y-%m-%d')+'/index.html'
    smtp.sendMail('devEops平台运维周报', msg, ['yz2@8531.cn'])#,'wzz@8531.cn','xubin@8531.cn','xuchenliang@8531.cn'])


def obj_maker(MODELS,dict_models):
    MODELS.objects.create(**dict_models)


@periodic_task(run_every=settings.EXPIRED_TIME)
def expired_aliyun_ecs():
    ExpiredAliyunECS.objects.all().delete()
    from deveops.tools.aliyun import ecs
    API = ecs.AliyunECSTool()
    for page in range(1,API.pagecount+1):
        results = API.get_instances(page)
        for result in results:
            dict_models = API.get_aliyun_expired_models(result)
            if dict_models.get('expired')< 20:
                obj_maker(ExpiredAliyunECS, dict_models)


@periodic_task(run_every=settings.EXPIRED_TIME)
def expired_aliyun_rds():
    ExpiredAliyunRDS.objects.all().delete()
    from deveops.tools.aliyun import rds
    API = rds.AliyunRDSTool()
    for page in range(1,API.pagecount+1):
        results = API.get_instances(page)
        for result in results:
            if not API.is_readonly(result):
                dict_models = API.get_aliyun_expired_models(result)
                if dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
                    obj_maker(ExpiredAliyunRDS,dict_models)

@periodic_task(run_every=settings.EXPIRED_TIME)
def expired_aliyun_kvstore():
    ExpiredAliyunKVStore.objects.all().delete()
    from deveops.tools.aliyun import kvstore
    API = kvstore.AliyunKVStoreTool()
    for page in range(1,API.pagecount+1):
        results = API.get_instances(page)
        for result in results:
            dict_models = API.get_aliyun_expired_models(result)
            if dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
                obj_maker(ExpiredAliyunKVStore,dict_models)


@periodic_task(run_every=settings.EXPIRED_TIME)
def expired_aliyun_mongodb():
    ExpiredAliyunMongoDB.objects.all().delete()
    from deveops.tools.aliyun import mongodb
    API = mongodb.AliyunMongoDBTool()
    for page in range(1,API.pagecount+1):
        results = API.get_instances(page)
        for result in results:
            dict_models = API.get_aliyun_expired_models(result)
            if dict_models.get('expired')< settings.ALIYUN_EXPIREDTIME:
                obj_maker(ExpiredAliyunMongoDB, dict_models)





