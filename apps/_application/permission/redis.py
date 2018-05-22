# from django.contrib.auth.mixins import AccessMixin
# from django.http import HttpResponseRedirect
# class RedisRequiredMixin(AccessMixin):
#     redirect_url= "/permission"
#     permission_required = u'application.all'
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
#         return super(RedisRequiredMixin, self).dispatch(request, *args, **kwargs)
#
# class RedisAddRequiredMixin(RedisRequiredMixin):
#     permission_required = u'application.add_redis'
#
# class RedisChangeRequiredMixin(RedisRequiredMixin):
#     permission_required = u'application.change_redis'
#
# class RedisDeleteRequiredMixin(RedisRequiredMixin):
#     permission_required = u'application.delete_redis'
