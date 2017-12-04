from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from rest_framework.permissions import BasePermission
class StorageRequiredMixin(AccessMixin):
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
        return super(StorageRequiredMixin, self).dispatch(request, *args, **kwargs)

class StorageAddRequiredMixin(StorageRequiredMixin):
    permission_required = u'manager.add_storage'

class StorageChangeRequiredMixin(StorageRequiredMixin):
    permission_required = u'manager.change_storage'

class StorageDeleteRequiredMixin(BasePermission):
    permission_required = u'manager.delete_storage'

    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if perms in perm_list:
            return True
        else:
            return False


