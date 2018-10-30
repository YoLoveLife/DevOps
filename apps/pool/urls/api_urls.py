from django.urls import path
from ..api import pool as PoolAPI
urlpatterns=[
    # Resource host api
    path(r'v1/list/bypage/', PoolAPI.PoolListAPI.as_view()),
]