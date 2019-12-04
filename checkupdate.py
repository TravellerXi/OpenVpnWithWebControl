#!/usr/bin/python
# coding:utf-8
import requests
import os

def checkupdate():
    version = requests.get('https://raw.githubusercontent.com/TravellerXi/OpenVpnWithWebControl/master/version/version')
    #version.encoding('utf-8')
    versionOnline = version.text.replace('.', '').replace('\n','')
    with open('version/version', 'r') as f:
        versionLocal = f.read()
    versionLocal = versionLocal.replace('.', '')
    if versionOnline > versionLocal:
        return(versionOnline)
    else:
        return(0)





def updateversion():
    version=requests.get('https://raw.githubusercontent.com/TravellerXi/OpenVpnWithWebControl/master/version/version')
    #version.encoding('utf-8')
    versionOnline=version.text
    versionOnlinecode=versionOnline.replace('.','').replace('\n','')
    print (str(versionOnline))
    versionlocal=''
    with open ('version/version','r') as f:
        versionLocal = versionlocal+f.read()
    versionLocal=versionLocal.replace('.','').replace('\n','')
    print('will print version local')
    print(versionLocal)
    print(type(versionLocal))
    print('will print online version')
    print(versionOnline)
    print(type(versionOnline))
    if versionOnlinecode>versionLocal:
        setence2 = 'mkdir -p /openvpnbackup/'+versionLocal
        print(setence2)
        os.system(setence2)

        setence3 = '\cp -R -f /openvpn/* /openvpnbackup/'+versionLocal+'/'
        print(setence3)
        os.system(setence3)

        setence4 = 'rm -rf /openvpnbackup/'+ versionLocal+'/backup'+'/'
        print(setence4)
        os.system(setence4)

        print('backup delete ok')
        updateZip=requests.get('https://github.com/TravellerXi/OpenVpnWithWebControl/archive/master.zip')
        with open ('master.zip','wb') as code:
            code.write(updateZip.content)
        os.system('unzip -o /openvpn/master.zip')
        os.system('\cp -R -f /openvpn/OpenVpnWithWebControl-master/* /openvpn/')
        os.system('rm -rf /openvpn/OpenVpnWithWebControl*')
        os.system('rm -rf /openvpn/master.zip')
        os.system('chmod +x /openvpn/*')
        return 1
    else:
        return 0
