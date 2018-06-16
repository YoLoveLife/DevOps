# -*- coding:utf-8 -*-
# !/usr/bin/env python3
# Time 18-5-15
# Author Yo
# Email YoLoveLife@outlook.com
import io
from paramiko.rsakey import RSAKey


def ssh_keygen():
    output = io.StringIO()
    try:
        key = RSAKey.generate(2048)
        key.write_private_key(output)
        private_key = output.getvalue()
        publick_key = '{HEAD} {KEY} {DOMAIN}'.format(HEAD='ssh-rsa', KEY=key.get_base64(), DOMAIN='yo@yolovelife.com')
    except IOError as e:
        raise IOError('gen_keys: there was an error writing to the file')
    return private_key,publick_key

if __name__ == '__main__':
    ssh_keygen()