from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings
__all__ = [
    "UserAPIRequiredMixin", "UserOpsListRequiredMixin", "UserCreateRequiredMixin",
    "UserListRequiredMixin", "UserDeleteRequiredMixin", "UserUpdateRequiredMixin",
]


class UserAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class UserOpsListRequiredMixin(UserAPIRequiredMixin):
    permission_required = u'authority.yo_list_opsuser'

    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class UserListRequiredMixin(UserAPIRequiredMixin):
    permission_required = u'authority.yo_list_user'


class UserCreateRequiredMixin(UserAPIRequiredMixin):
    permission_required = u'authority.yo_create_user'

    @decorator_api(settings.TIMELINE_USER_CREATE)
    def has_permission(self, request, view):
        return request, super(UserCreateRequiredMixin, self).has_permission(request, view)


class UserUpdateRequiredMixin(UserAPIRequiredMixin):
    permission_required = u'authority.yo_update_user'

    @decorator_api(settings.TIMELINE_USER_UPDATE)
    def has_permission(self, request, view):
        return request, super(UserUpdateRequiredMixin, self).has_permission(request, view)


class UserDeleteRequiredMixin(UserAPIRequiredMixin):
    permission_required = u'authority.yo_delete_user'

    @decorator_api(settings.TIMELINE_USER_DELETE)
    def has_permission(self, request, view):
        return request, super(UserDeleteRequiredMixin, self).has_permission(request, view)
