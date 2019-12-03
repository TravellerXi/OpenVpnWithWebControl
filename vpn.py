#!/usr/bin/python
# coding:utf-8
import os



def vpn_generator(username):
    os.system('cd /openvpn && ./auto.sh '+username+' && cp /root/'+username+'.ovpn '+'/openvpn/users/')
    return (1)