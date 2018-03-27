# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission

__all__ = [
    "SysTypeAPIRequiredMixin", "SysTypeListRequiredMixin", "SysTypeCreateRequiredMixin",
    "SysTypeUpdateRequiredMixin", "SysTypeDetailRequiredMixin", "SysTypeDeleteRequiredMixin"
]


class SysTypeAPIRequiredMixin(BasePermission):

    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class SysTypeListRequiredMixin(SysTypeAPIRequiredMixin):
    permission_required = u'manager.yo_list_systype'


class SysTypeCreateRequiredMixin(SysTypeAPIRequiredMixin):
    permission_required = u'manager.yo_create_systype'


class SysTypeUpdateRequiredMixin(SysTypeAPIRequiredMixin):
    permission_required = u'manager.yo_update_systype'


class SysTypeDetailRequiredMixin(SysTypeAPIRequiredMixin):
    permission_required = u'manager.yo_detail_systype'


class SysTypeDeleteRequiredMixin(SysTypeAPIRequiredMixin):
    permission_required = u'manager.yo_delete_systype'
