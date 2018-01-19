from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from rest_framework.permissions import BasePermission
class XMTRequiredMixin(AccessMixin):
    redirect_url= "/permission"
    permission_required = u'xmt.all'
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
        return super(XMTRequiredMixin, self).dispatch(request, *args, **kwargs)

class XMTAddRequiredMixin(XMTRequiredMixin):
    permission_required = u'xmt.add_xmt'
