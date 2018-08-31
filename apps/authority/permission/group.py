from rest_framework.permissions import BasePermission
from django.conf import settings
from timeline.decorator import decorator_api

__all__ = [
    "GroupAPIRequiredMixin", "GroupListRequiredMixin","GroupCreateRequiredMixin",
    "GroupUpdateRequiredMixin","GroupDeleteRequiredMixin"
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

    @decorator_api(settings.TIMELIME_PMNGROUP_CREATE)
    def has_permission(self, request, view):
        return request, super(GroupCreateRequiredMixin, self).has_permission(request, view)


class GroupUpdateRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'authority.yo_update_pmngroup'

    @decorator_api(settings.TIMELINE_PMNGROUP_UPDATE)
    def has_permission(self, request, view):
        return request, super(GroupUpdateRequiredMixin, self).has_permission(request, view)


class GroupDeleteRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'authority.yo_delete_pmngroup'

    @decorator_api(settings.TIMELINE_PMNGROUP_DELETE)
    def has_permission(self, request, view):
        return request, super(GroupDeleteRequiredMixin, self).has_permission(request, view)