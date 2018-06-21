# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab
from pyecharts import Pie
from deveops.conf import ALIYUN_PAGESIZE,REDIS_PORT,REDIS_SPACE,EXPIREDTIME
from deveops import settings
import redis, datetime, json, os
from deveops.utils import aliyun
from deveops.utils import resolver
from manager import models as ManagerModels
from ops import models as OpsModels
from authority import models as AuthModels
from dashboard.models import ExpiredAliyunECS,ExpiredAliyunRDS,ExpiredAliyunKVStore,ExpiredAliyunMongoDB
from tool import smtp

connect = redis.StrictRedis(port=REDIS_PORT,db=REDIS_SPACE)


@periodic_task(run_every=crontab(minute=30,hour=1,day_of_week="sunday"))
def weeklyDashboard():
    import jinja2
    loader = jinja2.FileSystemLoader(settings.BASE_DIR+'/apps/dashboard/docs/', encoding='utf-8')
    env = jinja2.Environment(loader=loader)
    template = env.get_template("week")

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
    smtp.sendMail('devEops平台运维周报', msg, ['yz2@8531.cn','wzz@8531.cn','xubin@8531.cn','xuchenliang@8531.cn'])


@periodic_task(run_every=crontab(minute=1,hour=1))
def aliyunECSExpiredInfoCatch():
    ExpiredAliyunECS.objects.all().delete()
    countNumber = aliyun.fetch_ECSPage()
    threadNumber = int(countNumber/ALIYUN_PAGESIZE)
    now = datetime.datetime.now()
    for num in range(1,threadNumber+2):
        data = aliyun.fetch_Instances(num)
        for dt in data:
            expiredTime = datetime.datetime.strptime(dt['ExpiredTime'],'%Y-%m-%dT%H:%MZ')
            if 0 < (expiredTime-now).days < EXPIREDTIME:
                dt['ExpiredDay'] = (expiredTime-now).days
                instance_data = resolver.AliyunECS2Json.decode(dt)
                instance_data.pop('os')
                ExpiredAliyunECS(**instance_data).save()


@periodic_task(run_every=crontab(minute=2,hour=1))
def aliyunRDSInfoCatch():
    ExpiredAliyunRDS.objects.all().delete()
    countNumber = aliyun.fetch_RDSPage()
    threadNumber = int(countNumber/ALIYUN_PAGESIZE)
    now = datetime.datetime.now()
    for num in range(1,threadNumber+2):
        data = aliyun.fetch_RDSs(num)
        for dt in data:
            if not dt['DBInstanceId'][0:2] == 'rr':
                expiredTime = datetime.datetime.strptime(dt['ExpireTime'],'%Y-%m-%dT%H:%M:%SZ')
                if 0 < (expiredTime - now).days < EXPIREDTIME:
                    dt['ExpiredDay'] = (expiredTime - now).days
                    ExpiredAliyunRDS(**resolver.AliyunRDS2Json.decode(dt)).save()


@periodic_task(run_every=crontab(minute=3,hour=1))
def aliyunKVStoreInfoCatch():
    ExpiredAliyunKVStore.objects.all().delete()
    countNumber = aliyun.fetch_KVStorePage()
    threadNumber = int(countNumber/ALIYUN_PAGESIZE)
    now = datetime.datetime.now()
    for num in range(1,threadNumber+2):
        data = aliyun.fetch_KVStores(num)
        for dt in data:
            expiredTime = datetime.datetime.strptime(dt['EndTime'],'%Y-%m-%dT%H:%M:%SZ')
            if 0 < (expiredTime - now).days < EXPIREDTIME:
                dt['ExpiredDay'] = (expiredTime - now).days
                ExpiredAliyunKVStore(**resolver.AliyunKVStore2Json.decode(dt)).save()


@periodic_task(run_every=crontab(minute=4,hour=1))
def aliyunMongoDBInfoCatch():
    ExpiredAliyunMongoDB.objects.all().delete()
    countNumber = aliyun.fetch_MongoDBPage()
    threadNumber = int(countNumber/ALIYUN_PAGESIZE)
    if threadNumber ==0:
        threadNumber= threadNumber+1
    now = datetime.datetime.now()
    for num in range(1,threadNumber+2):
        data = aliyun.fetch_MongoDBs(num)
        for dt in data:
            expiredTime = datetime.datetime.strptime(dt['ExpireTime'],'%Y-%m-%dT%H:%MZ')
            if 0 < (expiredTime - now).days < EXPIREDTIME:
                dt['ExpiredDay'] = (expiredTime - now).days
                ExpiredAliyunMongoDB(**resolver.AliyunMongoDB2Json.decode(dt)).save()


@periodic_task(run_every=crontab(minute=10,hour=1))
def managerStatusCatch():
    connect.delete('MANAGER_STATUS')

    status = {}
    # 資產計數
    from manager import models as Manager
    status['host_count'] = Manager.Host.objects.count()
    status['group_count'] = Manager.Group.objects.count()

    # 類型統計
    systypes = Manager.System_Type.objects.all()
    sys_list = []
    for sys in systypes:
        sys_list.append({'name': sys.name,'value': sys.hosts_detail.count()})
    status['systemtype'] = sys_list
    # 不同系统类型所涉及的主机个数

    positions = Manager.Position.objects.all()
    pos_list = []
    for pos in positions:
        pos_list.append({'name': pos.name,'value': pos.hosts_detail.count()})
    status['position'] = pos_list
    # 不同位置所涉及的主机个数

    groups = Manager.Group.objects.all()
    group_list = []
    for group in groups:
        group_list.append({'name': group.name,'value': group.hosts.count()})
    status['groups'] = group_list

    status_json = json.dumps(status)
    connect.set('MANAGER_STATUS',status_json)





