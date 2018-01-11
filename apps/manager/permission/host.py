# -*- coding:utf-8 -*-
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from rest_framework.permissions import BasePermission
from timeline.decorator.manager import decorator_manager
class HostRequiredMixin(AccessMixin):
    redirect_url= "/permission"
    permission_required = u'manager.all'

    def has_permission(self):
        perms = self.permission_required
        perm_list=list(self.request.user.get_all_permissions())
        if perms in perm_list:
            return True
        else:
            return False

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return HttpResponseRedirect(self.redirect_url)
        return super(HostRequiredMixin, self).dispatch(request, *args, **kwargs)

class HostAPIRequiredMixin(BasePermission):

    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False

class HostAddRequiredMixin(HostRequiredMixin):
    permission_required = u'manager.add_host'

class HostChangeRequiredMixin(HostRequiredMixin):
    permission_required = u'manager.change_host'

class HostPasswordRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.passwd_host'

class HostDeleteRequiredMixin(HostAPIRequiredMixin):
    permission_required = u'manager.delete_host'




