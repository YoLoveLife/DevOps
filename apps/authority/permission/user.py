from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
#__all__ = ['UserDeleteRequiredMixin','UserAddRequiredMixin','UserChangeRequiredMixin']
class UserRequiredMixin(AccessMixin):
    redirect_url= "/permission"
    permission_required = u'authority.all'
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
        return super(UserRequiredMixin, self).dispatch(request, *args, **kwargs)

class UserAddRequiredMixin(UserRequiredMixin):
    permission_required = u'authority.add_extenduser'

class UserChangeRequiredMixin(UserRequiredMixin):
    permission_required = u'authority.change_extenduser'

class UserDeleteRequiredMixin(UserRequiredMixin):
    permission_required = u'authority.delete_extenduser'

