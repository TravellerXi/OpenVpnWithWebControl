#!/usr/bin/python
# coding:utf-8
import hashlib
def md5(password):
    password=password.encode(encoding='utf-8')
    hashedPassword=hashlib.md5()
    hashedPassword.update(password)
    return (hashedPassword.hexdigest())
