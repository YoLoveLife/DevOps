# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-2-12
# Author Yo
# Email YoLoveLife@outlook.com
import paramiko
from six import StringIO
import sshpubkeys
import io
from paramiko.rsakey import RSAKey


def ssh_keygen():
    output = io.StringIO()
    try:
        key = RSAKey.generate(2048)
        key.write_private_key(output)
        private_key = output.getvalue()
        publick_key = '{HEAD} {KEY} {DOMAIN}'.format(HEAD='ssh-rsa', KEY=key.get_base64(), DOMAIN='deveops@yolovelife.com')
    except IOError as e:
        raise IOError('gen_keys: there was an error writing to the file')
    return private_key,publick_key


def ssh_private_key2obj(ssh_key):
    key = None
    try:
        key = paramiko.RSAKey.from_private_key(StringIO(ssh_key))
    except paramiko.SSHException:
        pass
    return key


def private_key_validator(ssh_key):
    if isinstance(ssh_key, bytes):
        try:
            ssh_key = ssh_key.decode("utf-8")
        except UnicodeDecodeError:
            return False

    key = ssh_private_key2obj(ssh_key)
    if key is None:
        return False
    else:
        return True


def public_key_validator(ssh_key):
    ssh = sshpubkeys.SSHKey(ssh_key)
    try:
        ssh.parse()
    except (sshpubkeys.InvalidKeyException, UnicodeDecodeError):
        return False
    except NotImplementedError as e:
        return False
    return True


