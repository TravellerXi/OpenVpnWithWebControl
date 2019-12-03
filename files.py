#!/usr/bin/python
# coding:utf-8
import os
root = os.getcwd()

def file_name(file_dir):
    filelist = ''
    for root, dirs, files in os.walk(file_dir):
        print(files)  # os.walk()所在目录的所有非目录文件名
        # print(type(files))
        files=str(files)
        files.replace("'", '')
        filelist=filelist+files
    return (filelist)




def Returnlist(dir):
    a = file_name(dir)
    b = a.replace('[', '').replace(']', '').replace("'", "").replace('.ovpn', '')
    return (b)