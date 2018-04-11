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
    permission_required = u'utils.yo_list_meta'


class MissionCreateRequiredMixin(MissionAPIRequiredMixin):
    permission_required = u'utils.yo_create_meta'


class MissionUpdateRequiredMixin(MissionAPIRequiredMixin):
    permission_required = u'utils.yo_update_meta'


class MissionDeleteRequiredMixin(MissionAPIRequiredMixin):
    permission_required = u'utils.yo_delete_meta'




