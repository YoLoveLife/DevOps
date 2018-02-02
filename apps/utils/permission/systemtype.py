# -*- coding:utf-8 -*-
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from rest_framework.permissions import BasePermission

# class SystemTypeRequiredMixin(AccessMixin):
#     redirect_url= "/permission"
#     permission_required = u'manager.all'
#
#     def has_permission(self):
#         perms = self.permission_required
#         perm_list=list(self.request.user.get_all_permissions())
#         if perms in perm_list:
#             return True
#         else:
#             return False
#
#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             return HttpResponseRedirect(self.redirect_url)
#         return super(SystemTypeRequiredMixin, self).dispatch(request, *args, **kwargs)


class SystemTypeAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class SystemTypeAddRequiredMixin(SystemTypeAPIRequiredMixin):
    permission_required = u'manager.create_jumper'


class SystemTypeChangeRequiredMixin(SystemTypeAPIRequiredMixin):
    permission_required = u'manager.change_jumper'


class SystemTypeDeleteRequiredMixin(SystemTypeAPIRequiredMixin):
    permission_required = u'manager.delete_jumper'




