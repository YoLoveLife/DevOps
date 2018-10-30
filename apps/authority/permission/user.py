# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework.permissions import BasePermission

__all__ = [
    "UserAPIRequiredMixin", "UserOpsListRequiredMixin", "UserCreateRequiredMixin",
    "UserListRequiredMixin", "UserDeleteRequiredMixin", "UserUpdateRequiredMixin",
]


class UserAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list = list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class UserOpsListRequiredMixin(UserAPIRequiredMixin):
    permission_required = u'authority.yo_list_opsuser'

    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list = list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class UserListRequiredMixin(UserAPIRequiredMixin):
    permission_required = u'authority.yo_list_user'


class UserCreateRequiredMixin(UserAPIRequiredMixin):
    permission_required = u'authority.yo_create_user'


class UserUpdateRequiredMixin(UserAPIRequiredMixin):
    permission_required = u'authority.yo_update_user'


class UserDeleteRequiredMixin(UserAPIRequiredMixin):
    permission_required = u'authority.yo_delete_user'

