# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from django.test import TestCase

__all__ = [

]


# class GroupTestCase(TestCase):
#     def setUp(self):
#         Group.objects.create(name='Testname',info='Testinfo')
#
#     def test_groupcreate(self):
#         group = Group.objects.get(name='Testname')
#         self.assertEqual(group.info,'Testinfo')
#
#     def test_groupupdate(self):
#         group = Group.objects.get(name='Testname')
#         group.info='Testinfo2'
#         group.save()
#         self.assertEqual(group.info,'Testinfo2')
#
#     def test_groupdelete(self):
#         Group.objects.filter(name='Testname').delete()
#         self.assertEqual(Group.objects.filter(name='Testname').count(),0)
#
# class StorageTestCase(TestCase):
#     def setUp(self):
#         Storage.objects.create(disk_size='1024GB',disk_path='//192.168.0.1/testdisk',info='testdisk')
#
#     def test_storagecreate(self):
#         storage=Storage.objects.get(disk_size='1024GB')
#         self.assertEqual(storage.disk_path,'//192.168.0.1/testdisk')
#
#     def test_storageupdate(self):
#         Storage.objects.filter(disk_size='1024GB').update(disk_path='//192.168.0.1/ddr')
#         storage = Storage.objects.get(disk_size='1024GB')
#         self.assertEqual(storage.disk_path,'//192.168.0.1/ddr')
#
#     def test_storagedelete(self):
#         Storage.objects.filter(disk_size='1024GB').delete()
#         self.assertEqual(Storage.objects.filter(disk_size='1024GB').count(),0)
#
# class System_TypeTestCase(TestCase):
#     def setUp(self):
#         System_Type.objects.create(name='CentOS6.5')
#
#     def test_systemtypecreate(self):
#         systemtype = System_Type.objects.get(name='CentOS6.5')
#         self.assertEqual(systemtype.name,'CentOS6.5')
#
#     def test_systemtypeupdate(self):
#         System_Type.objects.filter(name='CentOS6.5').update(name='CentOS6.6')
#         systemtype = System_Type.objects.get(name='CentOS6.6')
#         self.assertEqual(systemtype.name,'CentOS6.6')
#
#     def test_systemtypedelete(self):
#         System_Type.objects.filter(id=1).delete()
#         self.assertEqual(System_Type.objects.filter(id=1).count(),0)
#
# class HostTestCase(TestCase):
#     def setUp(self):
#         Group.objects.create(name='Testgroup',info='Testgroupinfo')
#         Storage.objects.create(disk_size='1024GB', disk_path='//192.168.0.1/testdisk', info='testdisk')
#         System_Type.objects.create(name='CentOS6.5')
#         groups = Group.objects.filter(name='Testgroup')
#         storages = Storage.objects.filter(disk_size='1024GB')
#         systemtype = System_Type.objects.filter(name='CentOS6.5').get()
#         host = Host.objects.create(
#                             service_ip='192.168.1.2',
#             connect_ip='192.168.1.3',server_position='VmWare',
#                             hostname='localhost.localdomain',
#                             sshpasswd='testpasswd',sshport='52000',coreness='36',
#                             memory='1024MB',root_disk='1024G',info='testinfo')
#         host.storages = storages
#         host.groups = groups
#         host.systemtype = systemtype
#         host.save()
#
#     def test_hostcreate(self):
#         host = Host.objects.get(connect_ip='192.168.1.2')
#         self.assertEqual(host.hostname,'localhost.localdomain')
#
#     def test_hostmany2many(self):
#         host = Host.objects.get(connect_ip='192.168.1.2')
#         self.assertEqual(host.groups.all()[0].name,'Testgroup')
#         self.assertEqual(host.storages.all()[0].disk_path,'//192.168.0.1/testdisk')
#
#     def test_storage_getallgroupname(self):
#         storage = Storage.objects.get(disk_size='1024GB')
#         self.assertEqual(storage.get_all_group_name(),'Testgroup')
#
#     def test_hostupdate(self):
#         Host.objects.filter(connect_ip='192.168.1.2').update(server_position='Position-1')
#         host = Host.objects.get(connect_ip='192.168.1.2')
#         self.assertEqual(host.server_position,'Position-1')
#
#     def test_hostdelete(self):
#         Host.objects.filter(connect_ip='192.168.1.2').delete()
#         self.assertEqual(Host.objects.filter(connect_ip='192.168.1.2').count(),0)