#!/usr/bin/python
# coding:utf-8
def title_setup_pc(title):
    htmlbasic = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head><meta name="keywords" content="网络管理系统"><meta name="description" content="网络管理系统"><meta name="author" content="Traveller"><meta name="robots" content="All">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width,height=device-height,inital-scale=1.0,maximum-scale=1.0,user-scalable=no;">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="format-detection" content="telephone=no"><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>""" + title+"""</title>"""
    return htmlbasic

def title_setup_mobile(title):
    htmlbasic="""
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><meta name="keywords" content="网络管理系统"><meta name="description" content="网络管理系统"><meta name="author" content="Traveller"><meta name="robots" content="All">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>"""+title+"""</title>
    
    """
    return htmlbasic
