from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
#__all__ = ['MusicAddRequiredMixin','MusicChangeRequiredMixin','MusicDeleteRequiredMixin']
class MusicRequiredMixin(AccessMixin):
    redirect_url= "/permission"
    permission_required = u'concert.all'

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
        return super(MusicRequiredMixin, self).dispatch(request, *args, **kwargs)

class MusicAddRequiredMixin(MusicRequiredMixin):
    permission_required = u'concert.add_music'

class MusicChangeRequiredMixin(MusicRequiredMixin):
    permission_required = u'concert.change_music'

class MusicDeleteRequiredMixin(MusicRequiredMixin):
    permission_required = u'concert.delete_music'

