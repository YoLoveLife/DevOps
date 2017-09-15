from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource script api
    url(r'^v1/script/$', api.ScriptListAPI.as_view()),

    url(r'^v1/script/(?P<pk>[0-9]+)/args/',api.ScriptArgsListAPI.as_view()),

    # Resource scriptargs api
    url(r'^v1/scriptargs/(?P<pk>[0-9]+)/create/',api.ScriptArgsCreateAPI.as_view()),
    url(r'^v1/scriptargs/(?P<pk>[0-9]+)/remove/',api.ScriptRemoveArgsAPI.as_view()),

    # Resource playbook api
    url(r'^v1/playbook/$', api.PlaybookListAPI.as_view()),
    url(r'^v1/playbook/(?P<pk>[0-9]+)/tasks/', api.PlaybookTasksListAPI.as_view()),
    #
    # # Resource task api
    url(r'^v1/task/(?P<pk>[0-9]+)/create/',api.TaskCreateAPI.as_view()),
    url(r'^v1/task/(?P<pk>[0-9]+)/remove/',api.TaskRemoveAPI.as_view()),
    url(r'^v1/task/(?P<pk>[0-9]+)/sort/',api.TaskSortAPI.as_view()),
]