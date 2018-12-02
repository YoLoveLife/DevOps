# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings
from django.db.models import Q
__all__ = [

]


class SafeWorkAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        groups = request.user.groups.filter(Q(name__icontains='safe')|Q(name__startwith="安全"))
        if not groups.exists():
            return False

        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class SafeWorkListRequiredMixin(SafeWorkAPIRequiredMixin):
    permission_required = u'work.yo_list_safework'


class SafeWorkCreateRequiredMixin(SafeWorkAPIRequiredMixin):
    permission_required = u'work.yo_create_safework'

    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list = list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False

class SafeWorkStatusRequiredMixin(SafeWorkAPIRequiredMixin):
    permission_required = u'work.yo_status_safework'

    def has_permission(self, request, view):
        return request, super(SafeWorkStatusRequiredMixin, self).has_permission(request, view)


