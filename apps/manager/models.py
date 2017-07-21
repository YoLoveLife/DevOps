from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
class Group(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    remark=models.CharField(max_length=100)

class Host(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default='localhost')
    group=models.ForeignKey(Group,default=1,related_name='host_set')
    sship=models.CharField(max_length=15,default='192.168.1.1')
    sshpasswd=models.CharField(max_length=100,default='000000')
    sshport=models.CharField(max_length=5,default='22')
