from django.urls import path
from ..api import file as FileAPI
from ..api import image as ImageAPI
urlpatterns=[
    # Resource file api
    path(r'v1/file/', FileAPI.UtilsFileListAPI.as_view()),
    path(r'v1/file/bypage/', FileAPI.UtilsFileListByPageAPI.as_view()),
    path(r'v1/file/create/', FileAPI.UtilsFileCreateAPI.as_view()),
    path(r'v1/file/<uuid:pk>/update/', FileAPI.UtilsFileUpdateAPI.as_view()),
    path(r'v1/file/<uuid:pk>/delete/', FileAPI.UtilsFileDeleteAPI.as_view()),

    # Resource image api
    path(r'v1/image/', ImageAPI.UtilsImageListAPI.as_view()),
    path(r'v1/image/bypage/', ImageAPI.UtilsImageListByPageAPI.as_view()),
    path(r'v1/image/create/', ImageAPI.UtilsImageCreateAPI.as_view()),
    path(r'v1/image/<uuid:pk>/delete/', ImageAPI.UtilsImageDeleteAPI.as_view()),
]