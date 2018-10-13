# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from manager.models import Group, Host
from authority.models import ExtendUser
import uuid
__all__ = [
    "Engine", "Truck",

]

class Engine(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    command = models.ForeignKey(META_CONTENT, on_delete=models.SET_NULL, null=True, related_name='engines')
    hosts = models.ManyToManyField(Host, blank=True, related_name='user_engines', verbose_name=_("trucks"))
    results = models.TextField()


class Truck(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(ExtendUser, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group_truck')
    engines = models.ManyToManyField(Engine, blank=True, related_name='truck', verbose_name=_("truck"))


class Terminal(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(Host, on_delete=models.SET_NULL, null=True, related_name='terminal')
    results = models.TextField()


