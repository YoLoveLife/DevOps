# -*- coding:utf-8 -*-
from django.test import TestCase,Client,LiveServerTestCase
from authority.models import ExtendUser
# Create your tests here.


#view test
class IndexPageTestCase(LiveServerTestCase):
    port = 8000
    def setUp(self):
        self.user=ExtendUser.objects.create(username='yz2',first_name='Yu',last_name='Zhou')
        self.user.set_password('testuser')
        self.user.save()
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')

    def test_indexpage(self):
        # response = self.c.get('/validate/login')
        response = self.c.get('/')
        self.assertEqual(response.status_code,302)

    def test_404page(self):
        self.c.force_login(self.user)
        response = self.c.get('/404')
        self.assertEqual(response.status_code,301)

    def test_permissionpage(self):
        response = self.c.get('/permission')
        self.assertEqual(response.status_code,301)