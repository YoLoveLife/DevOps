# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings

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
    permission_required = u'yodns.yo_list_dns'


class DNSCreateRequiredMixin(DNSAPIRequiredMixin):
    permission_required = u'yodns.yo_create_dns'

    def has_permission(self, request, view):
        return request, super(DNSCreateRequiredMixin, self).has_permission(request, view)


class DNSUpdateRequiredMixin(DNSAPIRequiredMixin):
    permission_required = u'yodns.yo_update_dns'

    def has_permission(self, request, view):
        return request, super(DNSUpdateRequiredMixin, self).has_permission(request, view)


class DNSDeleteRequiredMixin(DNSAPIRequiredMixin):
    permission_required = u'yodns.yo_delete_dns'

    def has_permission(self, request, view):
        return request, super(DNSDeleteRequiredMixin, self).has_permission(request, view)