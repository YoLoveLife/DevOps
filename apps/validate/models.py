from __future__ import unicode_literals


from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
# Create your models here.
class ExtendUser(AbstractUser):
    img = models.CharField(max_length=10,default='user.jpg')
    phone = models.CharField(max_length=11,default='18458409298')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s%s' % (self.first_name, self.last_name)
        return full_name.strip()