from rest_framework.permissions import BasePermission

__all__ = [
    "ExpiredAPIRequiredMixin", "ExpiredCreateRequiredMixin", "ExpiredChangeRequiredMixin",
    "ExpiredDeleteRequiredMixin"
]


class ExpiredAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class ExpiredListRequiredMixin(ExpiredAPIRequiredMixin):
    permission_required = u'dashboard.yo_list_expired'


class ExpiredCreateRequiredMixin(ExpiredAPIRequiredMixin):
    permission_required = u'dashboard.yo_create_expired'


class ExpiredUpdateRequiredMixin(ExpiredAPIRequiredMixin):
    permission_required = u'dashboard.yo_update_expired'


class ExpiredDeleteRequiredMixin(ExpiredAPIRequiredMixin):
    permission_required = u'dashboard.yo_delete_expired'

