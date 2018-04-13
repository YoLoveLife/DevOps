# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission

__all__ = [
    'CodeWorkAPIRequiredMixin', 'CodeWorkCreateRequiredMixin',
    'CodeWorkDeleteRequiredMixin', 'CodeWorkListRequiredMixin'
]


class CodeWorkAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class CodeWorkListRequiredMixin(CodeWorkAPIRequiredMixin):
    permission_required = u'work.yo_list_codework'


class CodeWorkCreateRequiredMixin(CodeWorkAPIRequiredMixin):
    permission_required = u'work.yo_create_codework'

class CodeWorkExamRequiredMixin(CodeWorkAPIRequiredMixin):
    permission_required = u'work.yo_exam_codework'

class CodeWorkDeleteRequiredMixin(CodeWorkAPIRequiredMixin):
    permission_required = u'work.yo_delete_codework'


