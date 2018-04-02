from rest_framework.permissions import BasePermission

__all__ = [
    "JumperAPIRequiredMixin", "JumperCreateRequiredMixin", "JumperChangeRequiredMixin",
    "JumperDeleteRequiredMixin"
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


class JumperUpdateRequiredMixin(JumperAPIRequiredMixin):
    permission_required = u'authority.yo_update_jumper'


class JumperDeleteRequiredMixin(JumperAPIRequiredMixin):
    permission_required = u'authority.yo_delete_jumper'

