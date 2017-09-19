# -*- coding:utf-8 -*-
from django.test import TestCase,Client,LiveServerTestCase
from validate.models import ExtendUser
# Create your tests here.

#model test
class ExtendUserTestCase(TestCase):
    def setUp(self):
        ExtendUser.objects.create(username='yz2',first_name='Yu',last_name='Zhou')

    def test_getfullname(self):
        user = ExtendUser.objects.get(username='yz2')
        self.assertEqual(user.get_full_name(),'YuZhou')

#view test
class LoginPageTestCase(LiveServerTestCase):
    def test_loginpage(self):
        c = Client()
        response = c.get('/validate/login')
        self.assertEqual(response.status_code,200)

class LoginPostTestCase(LiveServerTestCase):
    def setUp(self):
        ExtendUser.objects.create(username='yz2',first_name='Yu',last_name='Zhou',password='testlogin')

    def test_loginpost(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = c.post('/validate/login',{'username':'yz2','passwd':'testlogin'})
        self.assertEqual(response.status_code,200)

    def test_logoutpage(self):
        c = Client()
        response = c.get('/validate/logout')
        self.assertEqual(response.status_code,302)