# -*- coding:utf-8 -*-
# from django.test import TestCase
#
# # Create your tests here.
# from django.contrib.auth.models import Group

# from .. import models
# class ManagerTestCase(TestCase):
#     def setUp(self):
#         group = models.Group.objects.create(name='测试组',info='这是测试组')
#         storage = models.Storage.objects.create(disk_size='1024MB',disk_path='//192.168.1.1/testdisk',info='测试存储')
#         host = models.Host.objects.create(systemtype=0,manage_ip='192.168.1.1',service_ip='192.168.1.2',
#                                           outer_ip='192.168.1.3',server_position='机架上',hostname='test.yolovelife.com',
#                                           normal_user='testuser',sshpasswd='ddr',sshport='52000',
#                                           coreness='3',memory='1024MB',root_disk='26G',info='测试主机')
#     def test_host_ddr(self):
#         self.assertEqual(3,3)
# class ExtendUserTestCase(TestCase):
#     def setUp(self):
#         grp=Group.objects.get(name='普通用户')
#         models.ExtendUser.objects.create(username='testuser',first_name='test',last_name='name',group=grp)
#
#     def test_user_getfullname(self):
#         testuser = models.ExtendUser.objects.get(username='testuser')
#         self.assertEqual(testuser.get_full_name(),'testname')
#
#     def test_user_getgroupname(self):
#         testuser = models.ExtendUser.objects.get(username='testuser')
#         self.assertEqual(testuser.get_group_name(),'普通用户')