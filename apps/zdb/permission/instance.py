from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings
__all__ = [
    "DBInstanceAPIRequiredMixin", "DBInstanceCreateRequiredMixin", "DBInstanceListRequiredMixin",
    "DBInstanceDeleteRequiredMixin", "DBInstanceUpdateRequiredMixin",
]


class ZDBInstanceAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class ZDBInstanceListRequiredMixin(ZDBInstanceAPIRequiredMixin):
    permission_required = u'zdb.yo_list_db'


class ZDBInstanceCreateRequiredMixin(ZDBInstanceAPIRequiredMixin):
    permission_required = u'zdb.yo_create_db'

    def has_permission(self, request, view):
        return request, super(ZDBInstanceCreateRequiredMixin, self).has_permission(request, view)


class ZDBInstanceUpdateRequiredMixin(ZDBInstanceAPIRequiredMixin):
    permission_required = u'zdb.yo_update_db'

    def has_permission(self, request, view):
        return request, super(ZDBInstanceUpdateRequiredMixin, self).has_permission(request, view)


class ZDBInstanceDeleteRequiredMixin(ZDBInstanceAPIRequiredMixin):
    permission_required = u'zdb.yo_delete_db'

    def has_permission(self, request, view):
        return request, super(ZDBInstanceDeleteRequiredMixin, self).has_permission(request, view)

