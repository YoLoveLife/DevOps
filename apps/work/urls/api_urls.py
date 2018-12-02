from django.urls import path
from ..api import code as CodeAPI
from ..api import safe as SafeAPI
urlpatterns=[
    # Resource codework api
    path(r'v1/codework/bypage/', CodeAPI.CodeWorkListByPageAPI.as_view()),
    path(r'v1/codework/create/', CodeAPI.CodeWorkCreateAPI.as_view()),
    path(r'v1/codework/<uuid:pk>/check/', CodeAPI.CodeWorkCheckAPI.as_view()), # 审核
    path(r'v1/codework/<uuid:pk>/upload/', CodeAPI.CodeWorkUploadFileAPI.as_view()), # 上传文件
    path(r'v1/codework/<uuid:pk>/run/', CodeAPI.CodeWorkRunAPI.as_view()),# 运行
    path(r'v1/codework/<uuid:pk>/results/', CodeAPI.CodeWorkResultsAPI.as_view()), # 运行结果
    #
    # Resource safework api
    path(r'v1/safework/bypage/', SafeAPI.SafeWorkListByPageAPI.as_view()),
    path(r'v1/safework/create/', SafeAPI.SafeWorkCreateAPI.as_view()),
    path(r'v1/safework/<uuid:pk>/status/', SafeAPI.SafeWorkStatusAPI.as_view()),
]