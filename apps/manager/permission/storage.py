from rest_framework.permissions import BasePermission

__all__ = [
    "StorageAPIRequiredMixin", "StorageCreateRequiredMixin", "StorageUpdateRequiredMixin",
    "StorageDeleteRequiredMixin"
]


class StorageAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class StorageCreateRequiredMixin(StorageAPIRequiredMixin):
    permission_required = u'manager.yo_create_storage'


class StorageUpdateRequiredMixin(StorageAPIRequiredMixin):
    permission_required = u'manager.yo_update_storage'


class StorageDeleteRequiredMixin(StorageAPIRequiredMixin):
    permission_required = u'manager.yo_delete_storage'

