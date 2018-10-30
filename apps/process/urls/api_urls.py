from django.urls import path
from ..api import process as CDNAPI

urlpatterns=[
    # Resource host api
    path(r'v1/cdn/bypage/', CDNAPI.YoCDNListByPageAPI.as_view()),
    path(r'v1/cdn/create/', CDNAPI.YoCDNCreateAPI.as_view()),
]