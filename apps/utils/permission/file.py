# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission

__all__ = [
    'FileAPIRequiredMixin', 'FileCreateRequiredMixin',
    'FileDeleteRequiredMixin', 'FileListRequiredMixin'
]


class FileAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class FileListRequiredMixin(FileAPIRequiredMixin):
    permission_required = u'utils.yo_list_file'


class FileCreateRequiredMixin(FileAPIRequiredMixin):
    permission_required = u'utils.yo_create_file'


class FileDeleteRequiredMixin(FileAPIRequiredMixin):
    permission_required = u'utils.yo_delete_file'


