from rest_framework.permissions import BasePermission
from django.conf import settings
from timeline.decorator import decorator_api

__all__ = [
    "JumperAPIRequiredMixin", "JumperCreateRequiredMixin", "JumperUpdateRequiredMixin",
    "JumperDeleteRequiredMixin", "JumperListRequiredMixin", "JumperStatusRequiredMixin"
]


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


class JumperListRequiredMixin(JumperAPIRequiredMixin):
    permission_required = u'authority.yo_list_jumper'


class JumperCreateRequiredMixin(JumperAPIRequiredMixin):
    permission_required = u'authority.yo_create_jumper'

    def has_permission(self, request, view):
        return request, super(JumperCreateRequiredMixin, self).has_permission(request, view)


class JumperUpdateRequiredMixin(JumperAPIRequiredMixin):
    permission_required = u'authority.yo_update_jumper'

    def has_permission(self, request, view):
        return request, super(JumperUpdateRequiredMixin, self).has_permission(request, view)


class JumperDeleteRequiredMixin(JumperAPIRequiredMixin):
    permission_required = u'authority.yo_delete_jumper'

    def has_permission(self, request, view):
        return request, super(JumperDeleteRequiredMixin, self).has_permission(request, view)


class JumperStatusRequiredMixin(JumperAPIRequiredMixin):
    permission_required = u'authority.yo_status_jumper'

    def has_permission(self, request, view):
        return request, super(JumperStatusRequiredMixin, self).has_permission(request, view)