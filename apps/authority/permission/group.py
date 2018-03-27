from rest_framework.permissions import BasePermission

__all__ = [
    "GroupAPIRequiredMixin", "GroupCreateRequiredMixin", "GroupChangeRequiredMixin",
    "GroupDeleteRequiredMixin"
]


class GroupAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class GroupListRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'authority.yo_list_pmngroup'


class GroupCreateRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'authority.yo_create_pmngroup'


class GroupUpdateRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'authority.yo_update_pmngroup'


class GroupDeleteRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'authority.yo_delete_pmngroup'

