from celery.schedules import crontab
#
DASHBOARD_STATS_COUNT = crontab(hour="*",)

DASHBOARD_STATS_WORK = crontab(minute="*/30")

DASHBOARD_STATS_GROUP = crontab(minute="*/30")

MANAGER_HOST_TIME = crontab(minute='*/30',)

MANAGER_HOST_SSH_CHECK = crontab(minute='*/10')

MANAGER_HOST_LOAD_CHECK = crontab(minute='*/30')

MANAGER_HOST_DISK_CHECK = crontab(minute='*/15')

POOL_SLB = crontab(minute='*/30')

POOL_GATEWAY = crontab(minute='*/30')

POOL_HOST = crontab(minute='*/30')

YODNS_REFLUSH = crontab(minute='*/20')
#,day_of_week="sunday")


