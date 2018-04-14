# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission

__all__ = [
    'PushMissionAPIRequiredMixin', 'PushMissionCreateRequiredMixin',
    'PushMissionDeleteRequiredMixin', 'PushMissionListRequiredMixin',
    'PushMissionUpdateRequiredMixin',
]


class PushMissionAPIRequiredMixin(BasePermission):
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


class PushMissionListRequiredMixin(PushMissionAPIRequiredMixin):
    permission_required = u'ops.yo_list_pushmission'


class PushMissionCreateRequiredMixin(PushMissionAPIRequiredMixin):
    permission_required = u'ops.yo_create_pushmission'


class PushMissionUpdateRequiredMixin(PushMissionAPIRequiredMixin):
    permission_required = u'ops.yo_update_pushmission'


class PushMissionDeleteRequiredMixin(PushMissionAPIRequiredMixin):
    permission_required = u'ops.yo_delete_pushmission'




