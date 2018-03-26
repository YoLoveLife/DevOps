# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission

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

class HostListRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_list_host'

class HostPasswordRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_passwd_host'

class HostDeleteRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_delete_host'




