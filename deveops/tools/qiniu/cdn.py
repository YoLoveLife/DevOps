# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author WZZ
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()


from qiniu import CdnManager, Auth
from django.conf import settings

class QiNiuTool(object):
    pass


class QiNiuCDNTool(QiNiuTool):
    def __init__(self):
        self.manager = CdnManager(Auth(access_key=settings.QINIU_ACCESSKEY,
                                                 secret_key=settings.QINIU_ACCESSSECRET))

    def get_log_data(self):
        pass


    def check(self, url):
        if 'http' in url:
            index = url.find('//')
            header = url.find('/', index + 2)
            if '.' in url[header + 1:]: # uri
                return 'FILE'
            else:
                return 'DIR'
        else:
            index = url.find('/')
            if '.' in url[index+1:]:
                return 'FILE'
            else:
                return 'DIR'


    def sort(self, urls):
        file_urls = []
        dir_urls = []
        for url in urls:
            if self.check(url) == 'FILE':
                file_urls.append(url)
            else:
                dir_urls.append(url)

        return file_urls, dir_urls


    def refreshs(self, urls):
        file_urls, dir_urls = self.sort(urls)
        print(file_urls,dir_urls)
        if file_urls:
            ret, info= self.manager.refresh_dirs(dir_urls)
            print(ret, 'AAA',info)

        if dir_urls:
            ret, info =self.manager.refresh_urls(file_urls)
            print(ret, 'BBB',info)

    def refresh(self, url):
        ret = None
        info = None
        if self.check(url) == 'FILE':
            ret, info = self.manager.refresh_urls([url])
        else:
            ret, info = self.manager.refresh_dirs([url])

        if ret['code'] == 200:
            return True
        else:
            return False