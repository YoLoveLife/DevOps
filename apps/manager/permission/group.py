# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework.permissions import BasePermission
from django.conf import settings

__all__ = [
    "GroupAPIRequiredMixin", "GroupListRequiredMixin", "GroupCreateRequiredMixin",
    "GroupUpdateRequiredMixin", "GroupDetailRequiredMixin", "GroupDeleteRequiredMixin"
]


class GroupAPIRequiredMixin(BasePermission):

    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list = list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class GroupListRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'manager.yo_list_group'


class GroupCreateRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'manager.yo_create_group'


class GroupUpdateRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'manager.yo_update_group'


class GroupDetailRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'manager.yo_detail_group'


class GroupDeleteRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'manager.yo_delete_group'


class GroupSelectHostRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'manager.yo_group_sort_host'

