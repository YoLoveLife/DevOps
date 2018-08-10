from django.urls import path
from ezsetup.api import ezsetup as EZSetupAPI
urlpatterns=[
    # Resource EZSETUP Group Instance api
    path(r'v1/bypage/', EZSetupAPI.EZSetupListByPageAPI.as_view()),
    path(r'v1/mysql/create/', EZSetupAPI.EZSetupCreateMySQLAPI.as_view()),
    path(r'v1/redis/create/', EZSetupAPI.EZSetupCreateRedisAPI.as_view()),
]