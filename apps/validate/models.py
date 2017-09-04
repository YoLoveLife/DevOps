from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
class UserProfile(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User)
    img = models.CharField(max_length=10,default='user.jpg')
    phone = models.CharField(max_length=11,default='18458409298')

def create_user_profile(sender,instance,created,**kwargs):
    if created:
        profile=UserProfile()
        profile.user=instance
        profile.save()

post_save.connect(create_user_profile,sender=User)