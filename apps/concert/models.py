# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from operation.models import Script,PlayBook
from manager.models import Host,Group
# import timeline.models.ConcertHistory
# Create your models here.
#音符
__all__ = ['Note','Music']
class Note(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default='')
    scripts = models.ManyToManyField(Script,blank=True,related_name='scripts',verbose_name=_("Script"))
    playbook = models.ForeignKey(PlayBook,default=1,related_name="playbook_note")
    # hosts = models.ManyToManyField(Host,blank=True,related_name='host_notes',verbose_name=_("Host"))
    sort = models.IntegerField(default=0)


#乐谱 有多个Note
class Music(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default='')
    notes = models.ManyToManyField(Note,blank=True,related_name='note_musics',verbose_name=_("Note"))
    info = models.TextField(default='')#信息
    group = models.ForeignKey(Group,default=1,related_name="group_music")

    def get_last_use_info(self):
        return self.concert_his.order_by('endtime')[0].endtime
