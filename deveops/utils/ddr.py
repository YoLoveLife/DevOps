# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-26
# Author Yo
# Email YoLoveLife@outlook.com
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()

import atexit
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
from django.conf import settings as DJANGO_SETTINGS
si = connect.SmartConnectNoSSL(
    host=DJANGO_SETTINGS.VMWARE_SERVER,
    user=DJANGO_SETTINGS.VMWARE_USERNAME,
    pwd=DJANGO_SETTINGS.VMWARE_PASSWD,
    port=443
)

atexit.register(connect.Disconnect, si)

# search_index = si.content.searchIndex

content = si.RetrieveContent()
container = content.rootFolder
viewType = [vim.VirtualMachine]
recursive = True
containerView = content.viewManager.CreateContainerView(container, viewType, recursive)
children = containerView.view
count = 0
print(children)
for child in children:
    count = count + 1

print(count)


# vm = search_index.FindByUuid(None, '422691e4-0217-57c9-349b-6e5c17ec5602', True, True)
# if vm is None:
#     print('none')
# else:
#     print(vm.summary.config.name)