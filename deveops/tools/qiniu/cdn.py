# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author WZZ
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()


from qiniu import CdnManager, Auth, http
from django.conf import settings
import json

class QiNiuTool(object):
    pass


class QiNiuCDNTool(QiNiuTool):
    def __init__(self):
        self.manager = CdnManager(Auth(access_key=settings.QINIU_ACCESSKEY,
                                                 secret_key=settings.QINIU_ACCESSSECRET))
    @staticmethod
    def get_status(status):
        if status == 'success':
            return settings.STATUS_CDN_DONE
        elif status == 'processing':
            return settings.STATUS_CDN_RUN
        elif status == 'failure':
            return settings.STATUS_CDN_ERROR

    @staticmethod
    def get_models(result):
        return {
            'process': result['progress'],
            'status': QiNiuCDNTool.get_status(result['state']),
        }

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

    def tool_flush_cdn(self, url):
        ret = None
        info = None
        if self.check(url) == 'FILE':
            ret, info = self.manager.refresh_urls([url])
        else:
            ret, info = self.manager.refresh_dirs([url])

        return {
            'RefreshTaskId': ret['requestId'],
            'urlSurplusDay': ret['urlSurplusDay'],
            'dirQuotaDay': ret['dirQuotaDay'],
            'dirSurplusDay': ret['dirSurplusDay'],
            'urlQuotaDay': ret['urlQuotaDay'],
        }

    def tool_get_task(self, request_id):
        req = {}
        req['requestId'] = request_id
        body = json.dumps(req)
        url = '{0}/v2/tune/refresh/list'.format(self.manager.server)
        headers = {'Content-Type': 'application/json'}
        ret, info = http._post_with_auth_and_headers(url, body, self.manager.auth, headers)
        yield QiNiuCDNTool.get_models(ret['items'][0])



