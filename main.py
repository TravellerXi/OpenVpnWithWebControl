#!/usr/bin/python

# coding:utf-8

from flask import Flask,request,session,redirect,Response

#from flask_sqlalchemy import SQLAlchemy

import pymysql

#import upload.py

#from sso import *

from checkupdate import *

from vpn import *

from md5 import *

from htmlbase import *

from files import *

from flask import send_from_directory

import os

basedir = os.path.abspath(os.path.dirname(__file__))



app =Flask(__name__)





def Checkmd5(md5,username):

    db = pymysql.connect('localhost', 'openvpn', 'openvpn', 'openvpn')

    check = db.cursor()

    usernameSQL = 'select md5 from openvpn.user where username=' + "'" + username + "'"

    check.execute(usernameSQL)

    if (check.fetchone()) is None:

        db.close()

        return 0

    else:

        check.execute(usernameSQL)

        result=tuple(check.fetchone())

        result = ''.join(result)

        if md5 == result:

            db.close()

            return 2

        else:

            db.close()

            return 0





def ReturnUserlist():

    db = pymysql.connect('localhost', 'openvpn', 'openvpn', 'openvpn')

    check = db.cursor()

    usernameSQL = 'select username from openvpn.user'

    check.execute(usernameSQL)

    Strcheck = str(check.fetchall())

    Strcheck = Strcheck.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

    return (Strcheck)











def Checkisadmin(username):

    db = pymysql.connect('localhost', 'openvpn', 'openvpn', 'openvpn')

    check = db.cursor()

    usernameSQL = 'select isadmin from openvpn.user where username=' + "'" + username + "'"

    check.execute(usernameSQL)

    if (check.fetchone()) is None:

        db.close()

        return 0

    else:

        check.execute(usernameSQL)

        result=tuple(check.fetchone())

        result = ''.join(result)

        if result=='yes':

            db.close()

            return 2

        else:

            db.close()

            return 0





def CheckUsername(username):

    db = pymysql.connect('localhost', 'openvpn', 'openvpn', 'openvpn')

    check = db.cursor()

    usernameSQL = 'select username from openvpn.user where username=' + "'" + username + "'"

    check.execute(usernameSQL)

    if (check.fetchone()) is None:

        db.close()

        return 0

    else:

        check.execute(usernameSQL)

        result=tuple(check.fetchone())

        result = ''.join(result)

        if username == result:

            db.close()

            return 2

        else:

            db.close()

            return 0





def CheckPassword(username,password):

    db = pymysql.connect('localhost', 'openvpn', 'openvpn', 'openvpn')

    check = db.cursor()

    passwordSQL = 'select password from openvpn.user where username=' + "'" + username + "'"

    check.execute(passwordSQL)

    if check.fetchone() is None:

        db.close()

        return 0

    else:

        check.execute(passwordSQL)

        result=tuple(check.fetchone())

        result = ''.join(result)

        if password == result:

            db.close()

            return 2

        else:

            db.close()

            return 0



def inviteC():

    with open('static/invitecode','r',encoding='utf-8') as f:

        return(f.read())







@app.route('/', methods=['GET', 'POST'])

def home():

    with open('static/pcormobile.html','r',encoding='utf-8') as f:

        return(f.read())



 

@app.route('/introduce', methods=['GET'])

def introduce_post():

    with open('static/introuduce.html','r',encoding='utf-8') as f:

        return(f.read())



@app.route('/mobile/introduce', methods=['GET'])

def introduce_post_mobile():

    with open('static/introuduce.html','r',encoding='utf-8') as f:

        return(f.read())

  



@app.route('/signin', methods=['GET'])

def signin_form():

    user = request.cookies.get('username')

    md5credit = request.cookies.get('credit')

    if not md5credit:

        return (title_setup_pc('欢迎登录Openvpn管理系统')+'''<form action="/signin" method="post">

                              <p>用户名：<input name="username"></p>

                              <p>密码：&nbsp&nbsp&nbsp<input name="password" type="password"></p>

                              <p><button type="submit">Sign In</button></p>

                              <a href='/signup'target='_blank'>还没有账号？点此注册</a>

                              </form></html>''')

    else:

        result=Checkmd5(md5credit,user)

        if not result:

            return (title_setup_pc('欢迎登录Openvpn管理系统')+'''<form action="/signin" method="post">

                          <p>用户名：<input name="username"></p>

                          <p>密码：&nbsp&nbsp&nbsp<input name="password" type="password"></p>

                          <p><button type="submit">Sign In</button></p>

                          <a href='/signup'target='_blank'>还没有账号？点此注册</a>

                          </form>''')

        else:

            return redirect('/success')







@app.route('/signin', methods=['POST'])

def signin():

    # 需要从request对象读取表单内容：

    username=str(request.form['username'])

    password=str(request.form['password'])

    if CheckUsername(username) > 1:

        if CheckPassword(username,password) > 1:

            md5hash = md5(password)

            response=redirect('/success')

            response.set_cookie('username',username,max_age=7*24*3600)

            response.set_cookie('credit',md5hash,max_age=7*24*3600)

            return response



        else:

            return (title_setup_pc('error')+'<p>Bad password</p><br><a href="/signin">返回登录</a>')

    else:

        return (title_setup_pc('error')+'<p>Bad username</p><br><a href="/signin">返回登录</a>')



@app.route('/success', methods=['GET'])

def Success_login():

    user=request.cookies.get('username')

    md5credit=request.cookies.get('credit')

    if not md5credit:

        response = redirect('/signin')

        return response

    else:

        checkmd5 = Checkmd5(md5credit,user)

        if not checkmd5:

            response = redirect('/signin')

            return response

        else:

            if Checkisadmin(user) >0:

                if checkupdate() >0:

                    sourcecode = "<h3>Hello, 系统管理员: " + user + "!</h3><br><br>当前已注册VPN服务的用户列表>>>><br><br>" + ReturnUserlist() + "<br><br><a href='vpn'target='_blank'>获取/刷新VPN配置文件 (首次登陆请点此注册VPN服务)</a><br><a href='changepasswd'target='_blank'>修改我的密码</a><br><a href='deluser'target='_blank'>删除用户</a><br><a href='changeinvitecode'target='_blank'>修改邀请码(邀请码用于用户注册，默认openvpn，请务必修改)</a><br><a href='addadmin'target='_blank'>添加已注册用户为管理员</a><br><a href='updateversion'target='_blank'>网站后端可更新，点此更新，（不影响原有用户使用VPN）</a><br><br><a href='logout' >注销</a>"

                else:

                    sourcecode = "<h3>Hello, 系统管理员: " + user + "!</h3><br><br>当前已注册VPN服务的用户列表>>>><br><br>" + ReturnUserlist() + "<br><br><a href='vpn'target='_blank'>获取/刷新VPN配置文件 (首次登陆请点此注册VPN服务)</a><br><a href='changepasswd'target='_blank'>修改我的密码</a><br><a href='deluser'target='_blank'>删除用户</a><br><a href='changeinvitecode'target='_blank'>修改邀请码(邀请码用于用户注册，默认openvpn，请务必修改)</a><br><a href='addadmin'target='_blank'>添加已注册用户为管理员</a><br><br><a href='logout' >注销</a>"

            else:

                sourcecode = "<h3>Hello, " + user + "!</h3><br><a href='vpn'target='_blank'>获取/刷新VPN配置文件 (首次登陆请点此注册VPN服务)</a><br><a href='changepasswd'target='_blank'>修改我的密码</a><br><br><br><br><a href='logout' >注销</a>"

            return (title_setup_pc('主页')+sourcecode)



@app.route('/favicon.ico',methods=['GET'])

def get_fav():

    return app.send_static_file('favicon.ico')

##not return app.send_static_file('static/favicon.ico'), it will automatically use static/...



@app.route('/updateversion',methods=['GET'])

def updateversion_get():

    updateversion()

    return (title_setup_pc('升级成功')+'升级成功！请返回首页<br><a href="/">返回首页</a>')



@app.route('/deluser',methods=['GET'])

def deluser():

    user = request.cookies.get('username')

    md5credit = request.cookies.get('credit')

    if Checkmd5(md5credit,user)>0:

        return (title_setup_pc('删除用户') + '''<form action="/deluser" method="post">

                                  <p>用户名：&nbsp&nbsp&nbsp<input name="userid" ></p>

                                  <p><button type="submit">删除该用户</button></p>

                                  </form>''')

    else:

            return (title_setup_pc('error')+'用户未登陆！<br><a href="/signin">返回登录</a>&nbsp<a href="/signup">返回注册</a>')





@app.route('/deluser', methods=['POST'])

def deluser_post():

    # 需要从request对象读取表单内容：

    user = request.cookies.get('username')

    username=str(user)

    md5credit = request.cookies.get('credit')

    if Checkmd5(md5credit,user)>0:

        if Checkisadmin(user)>0:

            userid = str(request.form['userid'])

            db = pymysql.connect('localhost', 'openvpn', 'openvpn', 'openvpn')

            check = db.cursor()

            usernameSQL = "DELETE FROM openvpn.user WHERE username=" + "'" + userid + "'"

            check.execute(usernameSQL)

            db.commit()

            db.close()

            os.system('rm -rf /openvpn/users/' + userid + '.ovpn ')

            os.system('rm -rf /root/' + userid + '.ovpn ')

            return (title_setup_pc('删除用户成功') + '删除成功！<br><a href="/">返回首页</a>')

        else:

            return(title_setup_pc('无权操作')+'用户不是管理员，无权操作！<br><a href="/">返回首页</a>&nbsp<a href="/signup">返回注册</a>')

    else:

        return (title_setup_pc('error')+'用户未登陆！<br><a href="/signin">返回登录</a>&nbsp<a href="/signup">返回注册</a>')



@app.route('/addadmin',methods=['GET'])

def addadmin():

    user = request.cookies.get('username')

    md5credit = request.cookies.get('credit')

    if Checkmd5(md5credit,user)>0:

        return (title_setup_pc('提升已有用户为管理账号') + '''<form action="/addadmin" method="post">

                                  <p>已有用户名：&nbsp&nbsp&nbsp<input name="userid" ></p>

                                  <p><button type="submit">提升该用户为管理员</button></p>

                                  </form>''')

    else:

            return (title_setup_pc('error')+'用户未登陆！<br><a href="/signin">返回登录</a>&nbsp<a href="/signup">返回注册</a>')





@app.route('/addadmin', methods=['POST'])

def addadmin_post():

    # 需要从request对象读取表单内容：

    user = request.cookies.get('username')

    username=str(user)

    md5credit = request.cookies.get('credit')

    if Checkmd5(md5credit,user)>0:

        if Checkisadmin(user)>0:

            userid = str(request.form['userid'])

            db = pymysql.connect('localhost', 'openvpn', 'openvpn', 'openvpn')

            check = db.cursor()

            usernameSQL = "update openvpn.user set isadmin='yes' where username="+"'"+userid+"'"

            check.execute(usernameSQL)

            db.commit()

            db.close()

            os.system('rm -rf /openvpn/users/' + userid + '.ovpn ')

            os.system('rm -rf /root/' + userid + '.ovpn ')

            return (title_setup_pc('添加成功') + '添加管理员成功！<br><a href="/">返回首页</a>')

        else:

            return(title_setup_pc('无权操作')+'用户不是管理员，无权操作！<br><a href="/">返回首页</a>&nbsp<a href="/signup">返回注册</a>')

    else:

        return (title_setup_pc('error')+'用户未登陆！<br><a href="/signin">返回登录</a>&nbsp<a href="/signup">返回注册</a>')







@app.route('/changeinvitecode',methods=['GET'])

def changeinvitecode_get():

    user = request.cookies.get('username')

    md5credit = request.cookies.get('credit')

    if Checkmd5(md5credit,user)>0:

        return (title_setup_pc('修改邀请码') + '''<form action="/changeinvitecode" method="post">

                                  <p>新邀请码：&nbsp&nbsp&nbsp<input name="invitecode"></p>

                                  <p><button type="submit">修改</button></p>

                                  </form>''')

    else:

            return (title_setup_pc('error')+'用户未登陆！<br><a href="/signin">返回登录</a>&nbsp<a href="/signup">返回注册</a>')





@app.route('/changeinvitecode', methods=['POST'])

def changeinvitecode_post():

    # 需要从request对象读取表单内容：

    user = request.cookies.get('username')

    username=str(user)

    md5credit = request.cookies.get('credit')

    if Checkmd5(md5credit,user)>0:

        invitecode = str(request.form['invitecode'])

        with open('static/invitecode', 'w', encoding='utf-8') as f:

            f.write(invitecode)



        return (title_setup_pc('修改成功') + '邀请码修改成功！<br><a href="/">返回首页</a>')

    else:

        return (title_setup_pc('error')+'用户未登陆！<br><a href="/signin">返回登录</a>&nbsp<a href="/signup">返回注册</a>')











@app.route('/changepasswd',methods=['GET'])

def change_passwd():

    user = request.cookies.get('username')

    md5credit = request.cookies.get('credit')

    if Checkmd5(md5credit,user)>0:

        return (title_setup_pc('修改我的密码') + '''<form action="/changepasswd" method="post">

                                  <p>密码：&nbsp&nbsp&nbsp<input name="password"></p>

                                  <p><button type="submit">修改</button></p>

                                  </form>''')

    else:

            return (title_setup_pc('error')+'用户未登陆！<br><a href="/signin">返回登录</a>&nbsp<a href="/signup">返回注册</a>')





@app.route('/changepasswd', methods=['POST'])

def change_passwd_post():

    # 需要从request对象读取表单内容：

    user = request.cookies.get('username')

    username=str(user)

    md5credit = request.cookies.get('credit')

    if Checkmd5(md5credit,user)>0:

        password = str(request.form['password'])

        md5hash = md5(password)

        db = pymysql.connect('localhost', 'openvpn', 'openvpn', 'openvpn')

        check = db.cursor()

        usernameSQL = "update openvpn.user set password="+"'"+password+"'"+", md5="+"'"+md5hash+"'"+" where username="+"'"+username+"'"

        check.execute(usernameSQL)

        db.commit()

        db.close()

        return (title_setup_pc('修改成功') + '密码修改成功！<br><a href="/signin">返回登录</a>')

    else:

        return (title_setup_pc('error')+'用户未登陆！<br><a href="/signin">返回登录</a>&nbsp<a href="/signup">返回注册</a>')







@app.route('/logout',methods=['POST','GET'])

def logout():

    response=redirect('/logedout')

    response.delete_cookie('username')

    response.delete_cookie('credit')

    return response



@app.route('/logedout',methods=['GET'])

def logedout():

    return (title_setup_pc('注销页')+"<p>成功注销</p><br><a href='/signin'>返回登录</a>")



@app.route('/upload_photo', methods=['POST'])

def upload_photo():

    user = request.cookies.get('username')

    md5credit=request.cookies.get('credit')

    checkmd5 = md5(md5credit, user)

    if not checkmd5:

        return (title_setup_pc('error')+"没有登录<br><a href='/signin'>返回登录</a>")

    else:

        img = request.files.get('photo')

        if img is None:

            print('未上传文件')

        # username = request.form['name']

        path = basedir + "/static/photo/"

        # file_path = path + img.filename

        file_path = path + img.name + '.jpg'

        img.save(file_path)

        print('上传头像成功，上传的用户是：' + user)

        return ('OK！')











@app.route('/vpn',methods=['GET'])

def vpn_gene():

    user=request.cookies.get('username')

    md5credit = request.cookies.get('credit')

    if not md5credit:

        response = redirect('/signin')

        return response

    else:

        checkmd5 = Checkmd5(md5credit,user)

        if not checkmd5:

            response = redirect('/signin')

            return response

        else:

            url = vpn_generator(user)

            return (title_setup_pc('VPN相关')+'VPN配置文件已经生成，点下方链接下载<br>' + '<a href="download" target="_blank">下载您的专属配置文件</a><br><a href="introduce" target="_blank">点此查看如何下载客户端以及配置使用VPN</a>')



@app.route('/mobile/vpn',methods=['GET'])

def vpn_gene_mobile():

    user=request.cookies.get('username')

    md5credit = request.cookies.get('credit')

    if not md5credit:

        response = redirect('/signin')

        return response

    else:

        checkmd5 = Checkmd5(md5credit,user)

        if not checkmd5:

            response = redirect('/signin')

            return response

        else:

            url = vpn_generator(user)

            return (title_setup_mobile('VPN相关')+'VPN配置文件已经生成，点下方链接下载<br>' + '<a href="download" target="_blank">下载您的专属配置文件</a><br><a href="introduce" target="_blank">点此查看如何下载客户端以及配置使用VPN</a>')







@app.route('/signup', methods=['GET'])

def signup_form():

    user=request.cookies.get('username')

    md5credit = request.cookies.get('credit')

    if not md5credit: 

        return (title_setup_pc('注册')+'''<form action="/signup" method="post">

                              <p>用户名：<input name="username"></p>

                              <p>密码：&nbsp&nbsp&nbsp<input name="password" type="password"></p>

                              <p>邀请码：<input name="invitecode"></p>

                              <p><button type="submit">Sign up</button></p>

                              </form>''')

    else:

        checkmd5 = Checkmd5(md5credit,user)

        if not checkmd5:

            return (title_setup_pc('注册')+'''<form action="/signup" method="post">

                              <p>用户名：<input name="username"></p>

                              <p>密码：&nbsp&nbsp&nbsp<input name="password" type="password"></p>

                              <p>邀请码：<input name="invitecode"></p>

                              <p><button type="submit">Sign up</button></p>

                              </form>''')

        else:

            return redirect('/success')





@app.route('/signup', methods=['POST'])

def signup():

    # 需要从request对象读取表单内容：

    username=str(request.form['username'])

    password=str(request.form['password'])

    invitecode=str(request.form['invitecode'])

    if invitecode ==str(inviteC()):

        md5hash = md5(password)

        if CheckUsername(username)==0:

            db = pymysql.connect('localhost', 'openvpn', 'openvpn', 'openvpn')

            check = db.cursor()

            usernameSQL = "insert into openvpn.user (username,password,md5,isadmin) VALUES (" + "'" + username + "'" + "," + "'" + password + "'" + "," + "'" + md5hash + "'" +","+"'"+ "no"+"'"+")"

            print(usernameSQL)

            check.execute(usernameSQL)

            db.commit()

            db.close()

            return (title_setup_pc('注册成功')+'注册成功！<br><a href="/signin">返回登录</a>')

        else:

            return (title_setup_pc('error')+'用户名已存在！<br><a href="/signin">返回登录</a>&nbsp<a href="/signup">返回注册</a>')

    else:

        return(title_setup_pc('error')+'邀请码错误！<br><a href="/signin">返回登录</a>&nbsp<a href="/signup">返回注册</a>')



@app.route('/mobile/', methods=['GET', 'POST'])

def mobile_home():

    user=request.cookies.get('username')

    md5credit=request.cookies.get('credit')

    if not md5credit:

        return redirect('/mobile/signin')

    else:

        result = Checkmd5(md5credit, user)

        if not result:

            return redirect('/mobile/signin')

        else:

            return redirect('/mobile/success')



@app.route('/mobile/signin', methods=['GET'])

def signin_form_mobile():

    user = request.cookies.get('username')

    md5credit = request.cookies.get('credit')

    if not md5credit:

        return (title_setup_mobile('欢迎登录Openvpn管理系统')+'''<form action="/mobile/signin" method="post">

                              <p>用户名：<input name="username"></p>

                              <p>密码：&nbsp&nbsp&nbsp<input name="password" type="password"></p>

                              <p><button type="submit">Sign In</button></p>

                              <a href='/mobile/signup'target='_blank'>还没有账号？点此注册</a>

                              </form></html>''')

    else:

        result=Checkmd5(md5credit,user)

        if not result:

            return (title_setup_mobile('欢迎登录Openvpn管理系统')+'''<form action="/mobile/signin" method="post">

                          <p>用户名：<input name="username"></p>

                          <p>密码：&nbsp&nbsp&nbsp<input name="password" type="password"></p>

                          <p><button type="submit">Sign In</button></p>

                          <a href='/mobile/signup'target='_blank'>还没有账号？点此注册</a>

                          </form></html>''')

        else:

            return redirect('/mobile/success')







@app.route('/mobile/signin', methods=['POST'])

def signin_mobile():

    # 需要从request对象读取表单内容：

    username=str(request.form['username'])

    password=str(request.form['password'])

    if CheckUsername(username) > 1:

        if CheckPassword(username,password) > 1:

            md5hash = md5(password)

            response=redirect('/mobile/success')

            response.set_cookie('username',username,max_age=7*24*3600)

            response.set_cookie('credit',md5hash,max_age=7*24*3600)

            return response



        else:

            return (title_setup_mobile('错误页')+'<p>Bad password</p><br><a href="/">返回登录</a>')

    else:

        return (title_setup_mobile('错误页')+'<p>Bad username</p><br><a href="/">返回登录</a>')



@app.route('/mobile/success', methods=['GET'])

def Success_login_mobile():

    user=request.cookies.get('username')

    md5credit=request.cookies.get('credit')

    if not md5credit:

        response = redirect('/mobile/signin')

        return response

    else:

        checkmd5 = Checkmd5(md5credit,user)

        if not checkmd5:

            response = redirect('/mobile/signin')

            return response

        else:

            if Checkisadmin(user) > 0:

                sourcecode = "<h3>Hello, 系统管理员: " + user + "!</h3><br><br>当前已注册VPN服务的用户列表>>>><br><br>" + ReturnUserlist() + "<br><a href='vpn'target='_blank'><br><br>获取/刷新VPN配置文件 (首次登陆请点此注册VPN服务)</a><br><a href='../changepasswd'target='_blank'>修改我的密码</a><br><a href='deluser'target='_blank'>删除用户</a><br><a href='changeinvitecode'target='_blank'>修改邀请码(邀请码用于用户注册，默认openvpn，请务必修改)</a><br><a href='addadmin'target='_blank'>添加已注册用户为管理员</a><br><br><a href='logout' >注销</a>"

            else:

                sourcecode = "<h3>Hello, " + user + "!</h3><br><a href='vpn'target='_blank'>获取/刷新VPN配置文件 (首次登陆请点此注册VPN服务)</a><br><a href='../changepasswd'target='_blank'>修改我的密码</a><br><br><br><br><a href='logout' >注销</a>"

            return (title_setup_mobile('Openvpn管理系统') + sourcecode)













@app.route('/mobile/logout',methods=['POST','GET'])

def logout_mobile():

    response=redirect('/mobile/logedout')

    response.delete_cookie('username')

    response.delete_cookie('credit')

    return response



@app.route('/mobile/logedout',methods=['GET'])

def logedout_mobile():

    return (title_setup_mobile('注销')+"<p>成功注销</p><br><a href='/'>返回登录</a>")













@app.route('/mobile/signup', methods=['GET'])

def signup_form_mobile():

    user=request.cookies.get('username')

    md5credit = request.cookies.get('credit')

    if not md5credit:

        return (title_setup_mobile('欢迎注册Openvpn管理系统')+'''<form action="/mobile/signup" method="post">

                              <p>用户名：<input name="username"></p>

                              <p>密码：&nbsp&nbsp&nbsp<input name="password" type="password"></p>

                              <p>邀请码：<input name="invitecode"></p>

                              <p><button type="submit">Sign up</button></p>

                              </form>''')

    else:

        checkmd5 = Checkmd5(md5credit,user)

        if not checkmd5:

            return (title_setup_mobile('欢迎注册Openvpn管理系统')+'''<form action="/mobile/signup" method="post">

                              <p>用户名：<input name="username"></p>

                              <p>密码：&nbsp&nbsp&nbsp<input name="password" type="password"></p>

                              <p>邀请码：<input name="invitecode"></p>

                              <p><button type="submit">Sign up</button></p>

                              </form>''')

        else:

            return redirect('/mobile/success')





@app.route('/mobile/signup', methods=['POST'])

def signup_mobile():

    # 需要从request对象读取表单内容：

    username=str(request.form['username'])

    password=str(request.form['password'])

    invitecode=str(request.form['invitecode'])

    if invitecode ==str(inviteC()):

        md5hash = md5(password)

        if CheckUsername(username)==0:

            db = pymysql.connect('localhost', 'openvpn', 'openvpn', 'openvpn')

            check = db.cursor()

            usernameSQL = "insert into openvpn.user (username,password,md5,isadmin) VALUES (" + "'" + username + "'" + "," + "'" + password + "'" + "," + "'" + md5hash + "'"+","+"'" + 'no' + "'" + ")"

            check.execute(usernameSQL)

            db.commit()

            db.close()

            return (title_setup_mobile('注册成功页') + '注册成功！<br><a href="/">返回登录</a></html>')

        else:

            return (title_setup_mobile('错误')+'用户名已存在！<br><a href="/signin">返回登录</a>&nbsp<a href="/signup">返回注册</a>')

    else:

        return(title_setup_mobile('邀请码错误')+'邀请码错误！<br><a href="/">返回登录</a>&nbsp<a href="/mobile/signup">返回注册</a>')





@app.route('/download',methods=['GET'])

def downloadOvpn():

    user = request.cookies.get('username')

    return send_from_directory(r"/openvpn/users/", filename=str(user)+".ovpn", as_attachment=True)



@app.route('/mobile/download',methods=['GET'])

def downloadOvpn_mobile():

    user = request.cookies.get('username')

    return send_from_directory(r"/openvpn/users/", filename=str(user)+".ovpn", as_attachment=True)



@app.route('/download/<filename>',methods=['GET'])

def get_file_get(filename):

    return app.send_static_file(filename)



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80, debug=True,threaded=True)

