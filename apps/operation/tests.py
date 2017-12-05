# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from operation.models import Script,ScriptArgs
from authority.models import ExtendUser
# Create your tests here.
class ScriptTestCase(TestCase):
    def setUp(self):
        user = ExtendUser.objects.create(username='yz2', first_name='Yu', last_name='Zhou')
        script = Script.objects.create(name='noName',info='noUse',
                                       script='<p>hostname</p><p>cat /etc/hosts</p>',
                                       author=user,status=0)

    def test_scriptcreate(self):
        script = Script.objects.get(name='noName')
        self.assertEqual(script.info,'noUse')

    def test_scriptupdate(self):
        script = Script.objects.get(name='noName')
        script.status=1
        script.save()
        self.assertEqual(script.status,1)

    def test_scriptremove(self):
        Script.objects.filter(name='noName').delete()
        self.assertEqual(Script.objects.filter(name='noName').count(),0)

class ScriptArgsTestCase(TestCase):
    def setUp(self):
        user = ExtendUser.objects.create(username='yz2', first_name='Yu', last_name='Zhou')
        script = Script.objects.create(name='noName',info='noUse',
                                       script='<p>hostname</p><p>cat /etc/hosts</p>',
                                       author=user,status=0)
        ScriptArgs.objects.create(args_name='prefix',args_value='/usr/local',script=script)

    def test_scriptargscreate(self):
        scriptargs = ScriptArgs.objects.get(args_name='prefix')
        self.assertEqual(scriptargs.args_value,'/usr/local')

    def test_scriptargsupdate(self):
        ScriptArgs.objects.filter(args_name='prefix').update(args_value='/etc')
        scriptargs = ScriptArgs.objects.get(args_name='prefix')
        self.assertEqual(scriptargs.args_value,'/etc')

    def test_scriptargsdelete(self):
        ScriptArgs.objects.filter(args_name='prefix').delete()
        self.assertEqual(ScriptArgs.objects.filter(args_name='prefix').count(), 0)


    def test_scriptformat(self):
        Script.objects.get(name='noName').formatScript()
        self.assertEqual(1,1)