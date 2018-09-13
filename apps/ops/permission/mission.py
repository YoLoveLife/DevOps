# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings

__all__ = [
    "MissionAPIRequiredMixin", "MissionListRequiredMixin", "MissionCreateRequiredMixin",
    "MissionUpdateRequiredMixin", "MissionDeleteRequiredMixin",
]


class MissionAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        # 超级管理员通行
        if request.user.is_superuser:
            return True
        # 拥有权限通行
        if perms in perm_list:
            return True
        else:
            return False


class MissionListRequiredMixin(MissionAPIRequiredMixin):
    permission_required = u'ops.yo_list_mission'


class MissionCreateRequiredMixin(MissionAPIRequiredMixin):
    permission_required = u'ops.yo_create_mission'

    def has_permission(self, request, view):
        return request, super(MissionCreateRequiredMixin, self).has_permission(request, view)


class MissionUpdateRequiredMixin(MissionAPIRequiredMixin):
    permission_required = u'ops.yo_update_mission'

    def has_permission(self, request, view):
        return request, super(MissionUpdateRequiredMixin, self).has_permission(request, view)


class MissionDeleteRequiredMixin(MissionAPIRequiredMixin):
    permission_required = u'ops.yo_delete_mission'

    def has_permission(self, request, view):
        return request, super(MissionDeleteRequiredMixin, self).has_permission(request, view)



