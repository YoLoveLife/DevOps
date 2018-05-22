from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource update api123
    url(r'^v1/update/host/(?P<pk>[0-9]+)/', api.UpdateHostAPI.as_view()),
    url(r'^v1/catch/db/(?P<pk>[0-9]+)/status',api.CatchDBStatusAPI.as_view()),
]
