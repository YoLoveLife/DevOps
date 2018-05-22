from django.urls import path
from ..api import file as FileAPI
urlpatterns=[
    # Resource file api
    path(r'v1/file/', FileAPI.UtilsFileListAPI.as_view()),
    path(r'v1/file/bypage/', FileAPI.UtilsFileListByPageAPI.as_view()),
    path(r'v1/file/create/', FileAPI.UtilsFileCreateAPI.as_view()),
    path(r'v1/file/<uuid:pk>/delete/', FileAPI.UtilsFileDeleteAPI.as_view())
]