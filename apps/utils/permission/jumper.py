# -*- coding:utf-8 -*-
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from rest_framework.permissions import BasePermission
class JumperRequiredMixin(AccessMixin):
    redirect_url= "/permission"
    permission_required = u'utils.all'

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
        return super(JumperRequiredMixin, self).dispatch(request, *args, **kwargs)

class JumperAPIRequiredMixin(BasePermission):

    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False

class JumperAddRequiredMixin(JumperRequiredMixin):
    permission_required = u'utils.add_jumper'

class JumperChangeRequiredMixin(JumperRequiredMixin):
    permission_required = u'utils.change_jumper'

class JumperDeleteRequiredMixin(JumperAPIRequiredMixin):
    permission_required = u'utils.delete_jumper'




