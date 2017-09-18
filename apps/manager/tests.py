# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from manager.models import Group,Storage,Host
class AAAATestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(AAAATestCase,cls).setUpTestData()
        group = Group.objects.create(name='测试组',info='这是测试组')
        storage = Storage.objects.create(disk_size='1024MB',disk_path='//192.168.1.1/testdisk',info='测试存储')

    # def setUp(self):

        # host = Host.objects.create(systemtype=0,manage_ip='192.168.1.1',service_ip='192.168.1.2',
        #                            outer_ip='192.168.1.3',server_position='机架上',hostname='test.yolovelife.com',
        #                            normal_user='testuser',sshpasswd='ddr',sshport='52000',
        #                            coreness='3',memory='1024MB',root_disk='26G',info='测试主机')
    def test_host_ddr(self):
        self.assertEqual(3,3)