# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings

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


class HostListRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_list_host'


class HostCreateRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_create_host'

    def has_permission(self, request, view):
        return request, super(HostCreateRequiredMixin, self).has_permission(request, view)


class HostDetailRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_detail_host'


class HostUpdateRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_update_host'

    def has_permission(self, request, view):
        return request, super(HostUpdateRequiredMixin, self).has_permission(request, view)


class HostDeleteRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_delete_host'

    def has_permission(self, request, view):
        return request, super(HostDeleteRequiredMixin, self).has_permission(request, view)


class HostPasswordRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_passwd_host'


class HostSelectGroupRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.yo_host_sort_group'

    def has_permission(self, request, view):
        return request, super(HostSelectGroupRequiredMixin, self).has_permission(request, view)