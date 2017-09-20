# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from execute.models import Callback
# Create your tests here.
class CallbackTestCase(TestCase):
    def setUp(self):
        Callback.objects.create(info='ddddddddr')

    def test_callbackcreate(self):
        callback = Callback.objects.get(id=1)
        self.assertEqual(callback.info,'ddddddddr')

    def test_callbackupdate(self):
        Callback.objects.filter(info='ddddddddr').update(info='testtest')
        callback = Callback.objects.get(info='testtest')
        self.assertEqual(callback.info,'testtest')

    def test_callbackdelete(self):
        Callback.objects.filter(id=1).delete()
        self.assertEqual(Callback.objects.filter(id=1).count(), 0)
