# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from application.models import DB
from softlib.models import Softlib
from manager.models import Host
# Create your tests here.
# class DBTestCase(TestCase):
#     def setUp(self):
#         softlib = Softlib.objects.create(soft_type=2,soft_version='1.10.3')
#         host = Host.objects.create(systemtype=1,
#                             manage_ip='192.168.1.1',service_ip='192.168.1.2',
#                             outer_ip='192.168.1.3',server_position='VmWare',
#                             hostname='localhost.localdomain',normal_user='TestProd',
#                             sshpasswd='testpasswd',sshport='52000',coreness='36',
#                             memory='1024MB',root_disk='1024G',info='testinfo')
#
#         db = DB.objects.create(host=host,prefix='/usr/local/mysql',root_passwd='000000',
#                           normal_user='testlink',normal_passwd='testlink',
#                           softlib=softlib)
#
#     def test_dbcreate(self):
#         db = DB.objects.get(prefix='/usr/local/mysql')
#         self.assertEqual(db.normal_user,'testlink')
#
#     def test_dbupdate(self):
#         DB.objects.filter(prefix='/usr/local/mysql').update(normal_passwd='testlink2')
#         db = DB.objects.get(prefix='/usr/local/mysql')
#         self.assertEqual(db.normal_passwd,'testlink2')
#
#     def test_dbdelete(self):
#         DB.objects.filter(prefix='/usr/local/mysql').delete()
#         self.assertEqual(DB.objects.filter(prefix='/usr/local/mysql').count(),0)

