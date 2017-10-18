# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from validate.models import ExtendUser
# class PermissionGroup(Group):
#     def get_all_permission(self):
#         str = ""
#         for permission in self.permissions:
#             str += permission.name + ' '
#         return str
