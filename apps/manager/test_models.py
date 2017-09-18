# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-9-18
# Author Yo
# Email YoLoveLife@outlook.com
from manager.models import Group,Storage
from django.test import TestCase
class GroupTests(TestCase):
    def setUp(self):
        Group.objects.get_or_create(name='测试组',info='这是测试组')

    def test_list(self):
        group = Group.objects.get(name='测试组')
        self.assertEqual(group.info,'这是测试组')
