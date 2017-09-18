# -*- coding:utf-8 -*-
from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import Group
import models
class ExtendUserTestCase(TestCase):
    def setUp(self):
        grp=Group.objects.get(name='普通用户')
        models.ExtendUser.objects.create(username='testuser',first_name='test',last_name='name',group=grp)

    def test_user_getfullname(self):
        testuser = models.ExtendUser.objects.get(username='testuser')
        self.assertEqual(testuser.get_full_name(),'testname')

    def test_user_getgroupname(self):
        testuser = models.ExtendUser.objects.get(username='testuser')
        self.assertEqual(testuser.get_group_name(),'普通用户')