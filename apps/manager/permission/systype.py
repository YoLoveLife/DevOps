# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings

__all__ = [
    "SysTypeAPIRequiredMixin", "SysTypeListRequiredMixin", "SysTypeCreateRequiredMixin",
    "SysTypeUpdateRequiredMixin", "SysTypeDetailRequiredMixin", "SysTypeDeleteRequiredMixin"
]


class SysTypeAPIRequiredMixin(BasePermission):

    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class SysTypeListRequiredMixin(SysTypeAPIRequiredMixin):
    permission_required = u'manager.yo_list_systype'


class SysTypeCreateRequiredMixin(SysTypeAPIRequiredMixin):
    permission_required = u'manager.yo_create_systype'

    @decorator_api(settings.TIMELINE_SYSTYPE_CREATE)
    def has_permission(self, request, view):
        return request, super(SysTypeCreateRequiredMixin, self).has_permission(request, view)

class SysTypeUpdateRequiredMixin(SysTypeAPIRequiredMixin):
    permission_required = u'manager.yo_update_systype'

    @decorator_api(settings.TIMELINE_SYSTYPE_UPDATE)
    def has_permission(self, request, view):
        return request, super(SysTypeUpdateRequiredMixin, self).has_permission(request, view)


class SysTypeDetailRequiredMixin(SysTypeAPIRequiredMixin):
    permission_required = u'manager.yo_detail_systype'


class SysTypeDeleteRequiredMixin(SysTypeAPIRequiredMixin):
    permission_required = u'manager.yo_delete_systype'

    @decorator_api(settings.TIMELINE_SYSTYPE_DELETE)
    def has_permission(self, request, view):
        return request, super(SysTypeDeleteRequiredMixin, self).has_permission(request, view)