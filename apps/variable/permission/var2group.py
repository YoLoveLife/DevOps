# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission

__all__ = [
    "Var2GroupAPIRequiredMixin", "Var2GroupListRequiredMixin", "Var2GroupCreateRequiredMixin",
    "Var2GroupDeleteRequiredMixin",
]


class Var2GroupAPIRequiredMixin(BasePermission):
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


class Var2GroupListRequiredMixin(Var2GroupAPIRequiredMixin):
    permission_required = u'ops.yo_list_group_var'


class Var2GroupCreateRequiredMixin(Var2GroupAPIRequiredMixin):
    permission_required = u'ops.yo_change_group_var'


class Var2GroupDeleteRequiredMixin(Var2GroupAPIRequiredMixin):
    permission_required = u'ops.yo_delete_group_var'


