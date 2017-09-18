# -*- coding:utf-8 -*-
from django.test import TestCase
from validate.models import ExtendUser
# Create your tests here.
class ExtendUserTestCase(TestCase):
    def setUp(self):
        ExtendUser.objects.create(username='yz2',first_name='Yu',last_name='Zhou')

    def test_getfullname(self):
        user = ExtendUser.objects.get(username='yz2')
        self.assertEqual(user.get_full_name(),'YuZhou')