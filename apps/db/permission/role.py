from rest_framework.permissions import BasePermission

__all__ = [
    "DBRoleAPIRequiredMixin", "DBRoleCreateRequiredMixin", "DBRoleListRequiredMixin",
    "DBRoleDeleteRequiredMixin", "DBRoleUpdateRequiredMixin",
]


class DBRoleAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class DBRoleListRequiredMixin(DBRoleAPIRequiredMixin):
    permission_required = u'db.yo_list_db_role'


class DBRoleCreateRequiredMixin(DBRoleAPIRequiredMixin):
    permission_required = u'db.yo_create_db_role'


class DBRoleUpdateRequiredMixin(DBRoleAPIRequiredMixin):
    permission_required = u'db.yo_update_db_role'


class DBRoleDeleteRequiredMixin(DBRoleAPIRequiredMixin):
    permission_required = u'db.yo_delete_db_role'

