# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-28
# Author Yo
# Email YoLoveLife@outlook.com
import xlrd
from upload.models import GroupUpload
def AnalyzeHostFromExcel(group_id,filename):
    upload = GroupUpload.objects.filter(file='group_%s/%s'%(group_id,filename))
    workbook = xlrd.open_workbook(upload.get_full_path())
    table = workbook.sheets()[0]

