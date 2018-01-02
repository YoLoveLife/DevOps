from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from rest_framework.permissions import BasePermission
class GroupRequiredMixin(AccessMixin):
    redirect_url= "/permission"
    permission_required = u'manager.all'
    permission_denied_message = ''

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
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)

class GroupAddRequiredMixin(GroupRequiredMixin):
    permission_required = u'manager.add_group'

class GroupChangeRequiredMixin(GroupRequiredMixin):
    permission_required = u'manager.change_group'

class GroupDeleteRequiredMixin(BasePermission):
    permission_required = u'manager.delete_group'

    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if perms in perm_list:
            return True
        else:
            return False

