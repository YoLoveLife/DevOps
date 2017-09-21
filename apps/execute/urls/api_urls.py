from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource update api
    url(r'^v1/update/host/(?P<pk>[0-9]+)/', api.UpdateHostAPI.as_view()),
]