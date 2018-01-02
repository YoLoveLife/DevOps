# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-12
# Author Yo
# Email YoLoveLife@outlook.com
from Crypto.Cipher import AES
from binascii import b2a_hex,a2b_hex
# from deveops.settings import SECRET_KEY
SECRET_KEY = '1x$!#dwp2_6^tdgs1nv8pwgutbc#4m%#qaz!m!0h_f*%6fp+vt'
KEY = SECRET_KEY
KEY_LENGTH=16
def encrypt(text):
    # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
    cryptor = AES.new(KEY[0:KEY_LENGTH], AES.MODE_CBC, KEY[0:KEY_LENGTH])
    length = KEY_LENGTH
    count = len(text)
    add = length - (count % length)
    text = text + ('\0' * add)
    ciphertext = cryptor.encrypt(text)
    # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    # 所以这里统一把加密后的字符串转化为16进制字符串
    return b2a_hex(ciphertext)

def decrypt(text):
    cryptor = AES.new(KEY[0:16], AES.MODE_CBC, KEY[0:16])
    plain_text = cryptor.decrypt(a2b_hex(text))
    return plain_text.rstrip('\0')

if __name__ == '__main__':
    e = encrypt("daiSgmiku2")
    d = decrypt('508ffea1e80ee020d151d81b25fc56db')
    print e, d