from rest_framework.permissions import BasePermission

__all__ = [
    "DBUserAPIRequiredMixin", "DBUserCreateRequiredMixin", "DBUserListRequiredMixin",
    "DBUserDeleteRequiredMixin", "DBUserUpdateRequiredMixin",
]


class DBUserAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class DBUserListRequiredMixin(DBUserAPIRequiredMixin):
    permission_required = u'db.yo_list_db_user'


class DBUserCreateRequiredMixin(DBUserAPIRequiredMixin):
    permission_required = u'db.yo_create_db_user'


class DBUserUpdateRequiredMixin(DBUserAPIRequiredMixin):
    permission_required = u'db.yo_update_db_user'


class DBUserDeleteRequiredMixin(DBUserAPIRequiredMixin):
    permission_required = u'db.yo_delete_db_user'

