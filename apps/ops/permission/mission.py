# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission

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


class MissionUpdateRequiredMixin(MissionAPIRequiredMixin):
    permission_required = u'ops.yo_update_mission'


class MissionDeleteRequiredMixin(MissionAPIRequiredMixin):
    permission_required = u'ops.yo_delete_mission'




