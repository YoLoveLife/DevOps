from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings

__all__ = [
    "GroupAPIRequiredMixin", "GroupListRequiredMixin", "GroupCreateRequiredMixin",
    "GroupUpdateRequiredMixin", "GroupDetailRequiredMixin", "GroupDeleteRequiredMixin"
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
    permission_required = u'manager.yo_list_group'


class GroupCreateRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'manager.yo_create_group'

    @decorator_api(settings.TIMELINE_GROUP_CREATE)
    def has_permission(self, request, view):
        return request, super(GroupCreateRequiredMixin, self).has_permission(request, view)


class GroupUpdateRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'manager.yo_update_group'

    @decorator_api(settings.TIMELINE_GROUP_UPDATE)
    def has_permission(self, request, view):
        return request, super(GroupUpdateRequiredMixin, self).has_permission(request, view)


class GroupDetailRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'manager.yo_detail_group'


class GroupDeleteRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'manager.yo_delete_group'

    @decorator_api(settings.TIMELINE_GROUP_DELETE)
    def has_permission(self, request, view):
        return request, super(GroupDeleteRequiredMixin, self).has_permission(request, view)


class GroupSelectHostRequiredMixin(GroupAPIRequiredMixin):
    permission_required = u'manager.yo_group_sort_host'

    @decorator_api(settings.TIMELINE_GROUP_SORT)
    def has_permission(self, request, view):
        return request, super(GroupSelectHostRequiredMixin, self).has_permission(request, view)