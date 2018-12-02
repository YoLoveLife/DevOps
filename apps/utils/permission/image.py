# -*- coding:utf-8 -*-
from rest_framework.permissions import BasePermission
from timeline.decorator import decorator_api
from django.conf import settings

__all__ = [
    'ImageAPIRequiredMixin', 'ImageCreateRequiredMixin',
    'ImageDeleteRequiredMixin', 'ImageListRequiredMixin'
]


class ImageAPIRequiredMixin(BasePermission):
    def has_permission(self, request, view):
        perms = self.permission_required
        perm_list=list(request.user.get_all_permissions())
        if request.user.is_superuser:
            return True
        if perms in perm_list:
            return True
        else:
            return False


class ImageListRequiredMixin(ImageAPIRequiredMixin):
    permission_required = u'utils.yo_list_image'


class ImageCreateRequiredMixin(ImageAPIRequiredMixin):
    permission_required = u'utils.yo_create_image'

    def has_permission(self, request, view):
        return request, super(ImageCreateRequiredMixin, self).has_permission(request, view)


class ImageDeleteRequiredMixin(ImageAPIRequiredMixin):
    permission_required = u'utils.yo_delete_image'

    def has_permission(self, request, view):
        return request, super(ImageDeleteRequiredMixin, self).has_permission(request, view)
