from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings
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

    @decorator_api(settings.TIMELINE_DB_INSTANCE_CREATE)
    def has_permission(self, request, view):
        return request, super(DBInstanceCreateRequiredMixin, self).has_permission(request, view)


class DBInstanceUpdateRequiredMixin(DBInstanceAPIRequiredMixin):
    permission_required = u'db.yo_update_db'

    @decorator_api(settings.TIMELINE_DB_INSTANCE_UPDATE)
    def has_permission(self, request, view):
        return request, super(DBInstanceUpdateRequiredMixin, self).has_permission(request, view)


class DBInstanceDeleteRequiredMixin(DBInstanceAPIRequiredMixin):
    permission_required = u'db.yo_delete_db'

    @decorator_api(settings.TIMELINE_DB_INSTANCE_DELETE)
    def has_permission(self, request, view):
        return request, super(DBInstanceDeleteRequiredMixin, self).has_permission(request, view)

