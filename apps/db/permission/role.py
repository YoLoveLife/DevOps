from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings
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

    @decorator_api(settings.TIMELINE_DB_ROLE_CREATE)
    def has_permission(self, request, view):
        return request, super(DBRoleCreateRequiredMixin, self).has_permission(request, view)


class DBRoleUpdateRequiredMixin(DBRoleAPIRequiredMixin):
    permission_required = u'db.yo_update_db_role'

    @decorator_api(settings.TIMELINE_DB_ROLE_UPDATE)
    def has_permission(self, request, view):
        return request, super(DBRoleUpdateRequiredMixin, self).has_permission(request, view)


class DBRoleDeleteRequiredMixin(DBRoleAPIRequiredMixin):
    permission_required = u'db.yo_delete_db_role'

    @decorator_api(settings.TIMELINE_DB_ROLE_DELETE)
    def has_permission(self, request, view):
        return request, super(DBRoleDeleteRequiredMixin, self).has_permission(request, view)
