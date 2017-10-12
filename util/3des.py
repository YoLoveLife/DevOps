# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-12
# Author Yo
# Email YoLoveLife@outlook.com

from M2Crypto.EVP import Cipher

def encrypt_3des(key, text):
    encryptor = Cipher(alg='des_ede3_ecb', key=key, op=1, iv='\0'*16)
    s = encryptor.update(text)
    return s+ encryptor.final()

def decrypt_3des(key, text):
    decryptor = Cipher(alg='des_ede3_ecb', key=key, op=0, iv='\0'*16)
    s= decryptor.update(text)
    return s + decryptor.final()

if __name__ == "__main__":
    key = '1234567'
    passwd = 'daiSmgiku'
    decodepasswd =encrypt_3des(key, passwd)
    print(decodepasswd)
    passwd1 = decrypt_3des(key,decodepasswd)
    print(passwd1)
    # assert decrypt_3des(key, encrypt_text) == text