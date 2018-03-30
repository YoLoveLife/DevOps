# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 09 13:50
# Author Yo
# Email YoLoveLife@outlook.com
#!/usr/bin/env python
import os
import sys
# from django.conf import settings
if __name__ == "__main__":
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
    # os.environ['DJANGO_SETTINGS_MODULE'] = "deveops.settings"
    # print(sys.path)
    # reload(sys)
    # PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # sys.path.append(PROJECT_DIR)
    # print(sys.path)
    # PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # sys.path.append(PROJECT_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
    # reload(os)
    # print('environ',os.environ)
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)