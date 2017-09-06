from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
class PlaybookRequiredMixin(AccessMixin):
    redirect_url= "/permission"
    permission_required = u'operation.all_playbook'

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
        return super(PlaybookRequiredMixin, self).dispatch(request, *args, **kwargs)

class PlaybookAddRequiredMixin(PlaybookRequiredMixin):
    permission_required = u'operation.add_playbook'

class PlaybookChangeRequiredMixin(PlaybookRequiredMixin):
    permission_required = u'operation.change_playbook'

class PlaybookDeleteRequiredMixin(PlaybookRequiredMixin):
    permission_required = u'operation.delete_playbook'

