from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from rest_framework.permissions import BasePermission
class SoftlibRequiredMixin(AccessMixin):
    redirect_url= "/permission"
    permission_required = u'softlib.all'

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
        return super(SoftlibRequiredMixin, self).dispatch(request, *args, **kwargs)

class SoftlibAddRequiredMixin(SoftlibRequiredMixin):
    permission_required = u'softlib.add_softlib'

class SoftlibChangeRequiredMixin(SoftlibRequiredMixin):
    permission_required = u'softlib.change_softlib'

class SoftlibDeleteRequiredMixin(BasePermission):
    permission_required = u'softlib.delete_softlib'

    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if perms in perm_list:
            return True
        else:
            return False


