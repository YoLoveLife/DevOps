# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission

__all__ = [
    "DNSAPIRequiredMixin", "DNSListRequiredMixin", "DNSCreateRequiredMixin",
    "DNSUpdateRequiredMixin", "DNSDeleteRequiredMixin",
]


class DNSAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class DNSListRequiredMixin(DNSAPIRequiredMixin):
    permission_required = u'dns.yo_list_dns'


class DNSCreateRequiredMixin(DNSAPIRequiredMixin):
    permission_required = u'dns.yo_create_dns'


class DNSUpdateRequiredMixin(DNSAPIRequiredMixin):
    permission_required = u'dns.yo_update_dns'


class DNSDeleteRequiredMixin(DNSAPIRequiredMixin):
    permission_required = u'dns.yo_delete_dns'





