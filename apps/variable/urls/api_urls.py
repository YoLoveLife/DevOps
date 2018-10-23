from django.urls import path
from ..api import var2group as Var2GroupAPI

urlpatterns = [
    # Resource meta var2group
    path(r'v1/group/', Var2GroupAPI.Variable2GroupListAPI.as_view()),
    path(r'v1/group/create/', Var2GroupAPI.Variable2GroupCreateAPI.as_view()),
    path(r'v1/group/<uuid:pk>/delete/', Var2GroupAPI.Variable2GroupDeleteAPI.as_view()),
]