from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings

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

    @decorator_api(settings.TIMELINE_DB_USER_CREATE)
    def has_permission(self, request, view):
        return request, super(DBUserCreateRequiredMixin, self).has_permission(request, view)


class DBUserUpdateRequiredMixin(DBUserAPIRequiredMixin):
    permission_required = u'db.yo_update_db_user'

    @decorator_api(settings.TIMELINE_DB_USER_UPDATE)
    def has_permission(self, request, view):
        return request, super(DBUserUpdateRequiredMixin, self).has_permission(request, view)


class DBUserDeleteRequiredMixin(DBUserAPIRequiredMixin):
    permission_required = u'db.yo_delete_db_user'

    @decorator_api(settings.TIMELINE_DB_USER_DELETE)
    def has_permission(self, request, view):
        return request, super(DBUserDeleteRequiredMixin, self).has_permission(request, view)

