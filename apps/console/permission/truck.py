# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings

__all__ = [

]


class TruckAPIRequiredMixin(BasePermission):
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


class TruckCreateRequiredMixin(TruckAPIRequiredMixin):
    permission_required = u'console.yo_create_truck'

    @decorator_api(settings.TIMELINE_CONSOLE_TRUCK_CREATE)
    def has_permission(self, request, view):
        return request, super(TruckCreateRequiredMixin, self).has_permission(request, view)


