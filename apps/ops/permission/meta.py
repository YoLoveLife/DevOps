# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings

__all__ = [
    "MetaAPIRequiredMixin", "MetaListRequiredMixin", "MetaCreateRequiredMixin",
    "MetaUpdateRequiredMixin", "MetaDeleteRequiredMixin",
]


class MetaAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        # 超级管理员通行
        if request.user.is_superuser:
            return True
        # 拥有权限通行
        if perms in perm_list:
            return True
        else:
            return False


class MetaListRequiredMixin(MetaAPIRequiredMixin):
    permission_required = u'ops.yo_list_meta'


class MetaCreateRequiredMixin(MetaAPIRequiredMixin):
    permission_required = u'ops.yo_create_meta'

    @decorator_api(settings.TIMELINE_META_CREATE)
    def has_permission(self, request, view):
        return request, super(MetaCreateRequiredMixin, self).has_permission(request, view)


class MetaUpdateRequiredMixin(MetaAPIRequiredMixin):
    permission_required = u'ops.yo_update_meta'

    @decorator_api(settings.TIMELINE_META_UPDATE)
    def has_permission(self, request, view):
        return request, super(MetaUpdateRequiredMixin, self).has_permission(request, view)


class MetaDeleteRequiredMixin(MetaAPIRequiredMixin):
    permission_required = u'ops.yo_delete_meta'

    @decorator_api(settings.TIMELINE_META_DELETE)
    def has_permission(self, request, view):
        return request, super(MetaDeleteRequiredMixin, self).has_permission(request, view)



