from django.urls import path
from ..api import work as WorkAPI
urlpatterns=[
    # Resource codework api
    path(r'v1/codework/bypage/', WorkAPI.CodeWorkListByPageAPI.as_view()),
    path(r'v1/codework/create/', WorkAPI.CodeWorkCreateAPI.as_view()),
    path(r'v1/codework/<uuid:pk>/check/', WorkAPI.CodeWorkCheckAPI.as_view()),
    path(r'v1/codework/<uuid:pk>/run/', WorkAPI.CodeWorkRunAPI.as_view()),
]