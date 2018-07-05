from rest_framework.permissions import BasePermission

__all__ = [
    "DBInstanceAPIRequiredMixin", "DBInstanceCreateRequiredMixin", "DBInstanceListRequiredMixin",
    "DBInstanceDeleteRequiredMixin", "DBInstanceUpdateRequiredMixin",
]


class DBInstanceAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class DBInstanceListRequiredMixin(DBInstanceAPIRequiredMixin):
    permission_required = u'db.yo_list_db'


class DBInstanceCreateRequiredMixin(DBInstanceAPIRequiredMixin):
    permission_required = u'db.yo_create_db'


class DBInstanceUpdateRequiredMixin(DBInstanceAPIRequiredMixin):
    permission_required = u'db.yo_update_db'


class DBInstanceDeleteRequiredMixin(DBInstanceAPIRequiredMixin):
    permission_required = u'db.yo_delete_db'

