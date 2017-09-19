# -*- coding:utf-8 -*-
from django.test import TestCase,Client,LiveServerTestCase
# from validate.models import ExtendUser
# Create your tests here.


#view test
# class IndexPageTestCase(LiveServerTestCase):
#     port = 8000
#     def setUp(self):
#         self.user=ExtendUser.objects.create(username='yz2',first_name='Yu',last_name='Zhou')
#         self.user.set_password('testuser')
#         self.user.save()
#         self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')
#         self.c.login(username='yz2',password='testuser')
#         self.c.force_login(self.user)
#
#     def test_indexpage(self):
#         response = self.c.get('/')
#         self.assertEqual(response.status_code,200)
#
#     def test_404page(self):
#         response = self.c.get('/404')
#         self.assertEqual(response.status_code,301)
#
#     def test_permissionpage(self):
#         response = self.c.get('/permission')
#         self.assertEqual(response.status_code,301)