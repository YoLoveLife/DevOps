# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings

__all__ = [
    "PositionAPIRequiredMixin", "PositionListRequiredMixin", "PositionCreateRequiredMixin",
    "PositionUpdateRequiredMixin", "PositionDetailRequiredMixin", "PositionDeleteRequiredMixin"
]


class PositionAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class PositionListRequiredMixin(PositionAPIRequiredMixin):
    permission_required = u'manager.yo_list_position'


class PositionCreateRequiredMixin(PositionAPIRequiredMixin):
    permission_required = u'manager.yo_create_position'

    @decorator_api(settings.TIMELINE_POSITION_CREATE)
    def has_permission(self, request, view):
        return request, super(PositionCreateRequiredMixin, self).has_permission(request, view)

class PositionUpdateRequiredMixin(PositionAPIRequiredMixin):
    permission_required = u'manager.yo_update_position'

    @decorator_api(settings.TIMELINE_POSITION_UPDATE)
    def has_permission(self, request, view):
        return request, super(PositionUpdateRequiredMixin, self).has_permission(request, view)

class PositionDetailRequiredMixin(PositionAPIRequiredMixin):
    permission_required = u'manager.yo_detail_position'


class PositionDeleteRequiredMixin(PositionAPIRequiredMixin):
    permission_required = u'manager.yo_delete_position'

    @decorator_api(settings.TIMELINE_POSITION_DELETE)
    def has_permission(self, request, view):
        return request, super(PositionDeleteRequiredMixin, self).has_permission(request, view)