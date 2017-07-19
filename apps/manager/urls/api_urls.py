from django.conf.urls import url, include
from rest_framework import routers
from .. import api

router=routers.DefaultRouter()
router.register(r'host',api.HostViewSet)
router.register(r'group',api.GroupViewSet)

urlpatterns=router.urls
