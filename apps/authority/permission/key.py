# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework.permissions import BasePermission

__all__ = [
    "KeyAPIRequiredMixin", "KeyListRequiredMixin", "KeyCreateRequiredMixin",
    "KeyUpdateRequiredMixin", "KeyDeleteRequiredMixin",
]


class KeyAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list = list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class KeyListRequiredMixin(KeyAPIRequiredMixin):
    permission_required = u'authority.yo_list_key'


class KeyCreateRequiredMixin(KeyAPIRequiredMixin):
    permission_required = u'authority.yo_create_key'


class KeyUpdateRequiredMixin(KeyAPIRequiredMixin):
    permission_required = u'authority.yo_update_key'


class KeyDeleteRequiredMixin(KeyAPIRequiredMixin):
    permission_required = u'authority.yo_delete_key'

