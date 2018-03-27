# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission

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


class PositionUpdateRequiredMixin(PositionAPIRequiredMixin):
    permission_required = u'manager.yo_update_position'


class PositionDetailRequiredMixin(PositionAPIRequiredMixin):
    permission_required = u'manager.yo_detail_position'


class PositionDeleteRequiredMixin(PositionAPIRequiredMixin):
    permission_required = u'manager.yo_delete_position'
