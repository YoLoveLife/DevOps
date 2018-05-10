from django.conf.urls import url
from ..api import var2group as Var2GroupAPI
urlpatterns=[
    # Resource meta var2group
    url(r'^v1/group/$', Var2GroupAPI.Variable2GroupListAPI.as_view()),
    url(r'^v1/group/create/$', Var2GroupAPI.Variable2GroupCreateAPI.as_view()),
    url(r'^v1/group/(?P<pk>[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/delete/$', Var2GroupAPI.Variable2GroupDeleteAPI.as_view()),
]