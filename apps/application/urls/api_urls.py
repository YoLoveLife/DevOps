from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource db api
    url(r'^v1/db/', api.DBListAPI.as_view()),
]