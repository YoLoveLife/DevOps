# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings

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

    def has_permission(self, request, view):
        return request, super(CodeWorkCreateRequiredMixin, self).has_permission(request, view)

class CodeWorkExamRequiredMixin(CodeWorkAPIRequiredMixin):
    permission_required = u'work.yo_exam_codework'

    def has_permission(self, request, view):
        return request, super(CodeWorkExamRequiredMixin, self).has_permission(request, view)


class CodeWorkUploadRequiredMixin(CodeWorkAPIRequiredMixin):
    permission_required = u'work.yo_upload_codework'

    def has_permission(self, request, view):
        return request, super(CodeWorkUploadRequiredMixin, self).has_permission(request, view)


class CodeWorkRunRequiredMixin(CodeWorkAPIRequiredMixin):
    permission_required = u'work.yo_run_codework'

    def has_permission(self, request, view):
        return request, super(CodeWorkRunRequiredMixin, self).has_permission(request, view)


class CodeWorkDeleteRequiredMixin(CodeWorkAPIRequiredMixin):
    permission_required = u'work.yo_delete_codework'

    def has_permission(self, request, view):
        return request, super(CodeWorkDeleteRequiredMixin, self).has_permission(request, view)


class CodeWorkResultsRequiredMixin(CodeWorkAPIRequiredMixin):
    permission_required = u'work.yo_results_codework'

    def has_permission(self, request, view):
        return request, super(CodeWorkResultsRequiredMixin, self).has_permission(request, view)