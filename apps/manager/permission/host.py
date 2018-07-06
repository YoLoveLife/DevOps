# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission

__all__ = [
    "HostAPIRequiredMixin", "HostListRequiredMixin", "HostCreateRequiredMixin",
    "HostDetailRequiredMixin", "HostUpdateRequiredMixin", "HostDeleteRequiredMixin",
    "HostPasswordRequiredMixin"
]


class HostAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False

    # def has_object_permission(self, request, view, obj):


class HostListRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_list_host'


class HostCreateRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_create_host'


class HostDetailRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_detail_host'


class HostUpdateRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_update_host'


class HostDeleteRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_delete_host'


class HostPasswordRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_passwd_host'




