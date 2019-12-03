# coding:utf-8
# OpenVpnWithWebControl
OpenVpnWithWebControl

<a href="https://996.icu"><img src="https://img.shields.io/badge/link-996.icu-red.svg" alt="996.icu" /></a>


###这是一款提供web管理界面的OPENVPN，功能包括但不限于（仍在开发）：

#1.管理员登录。

#2.用户登录

#3 管理员添加，删除用户。添加管理员。

#4. 用户自助下载，配置VPN.



以下是安装本软件方法：


###必读：

#环境：Centos 6.5

#Python 3，在下述安装中，使用Python3.6.5，其他Python3版本亦可。（也就是说如果安装了Python3，您可以跳过Python3，安装，只需执行pip3 install flask pymysql paramiko requests）

#数据库采用Mysql，默认创建用户openvpn，密码openvpn，建立本地数据库openvpn。


###安装必要组件，下载源码和创建文件夹


yum -y install gcc

mkdir /openvpn

yum install -y mysql-server mysql mysql-devel

yum install -y wget unzip

yum upgrade -y curl

yum install -y wget

yum install -y ncurses-devel libuuid-devel zlib zlib-devel sqlite-devel readline-devel tkinter tcl-devel tk-devel lzma libgdbm-dev xz-devel

yum -y install bzip2-devel sqlite-devel openssl-devel readline-devel xz-devel xz-devel tk-devel gdbm-devel

yum -y install openssl openssl-devel

yum install -y expect

yum install libffi-devel -y

yum install unzip -y

vi /etc/sysconfig/iptables


###在'-A INPUT'第一行加一句(ACCEPT一定要在REJECT语句之前)：

-A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT

####

service iptables restart


cd /openvpn

wget https://codeload.github.com/TravellerXi/OpenVpnWithWebControl/zip/master

unzip master

\cp -R -f OpenVpnWithWebControl-master/* /openvpn/



###安装OPENVPN核心组件

cd /openvpn

chmod +x openvpn-install.sh

bash openvpn-install.sh

####上面这个命令一路回车即可

#如果遇到以下错误：

Error: Cannot retrieve metalink for repository: epel. Please verify its path and try again  


请修改/etc/yum.repos.d/epel.repo文件中的mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=epel-6&arch=$basearch (改为http)，具体操作：

vi /etc/yum.repos.d/epel.repo (改，然后保存)

yum clean all && yum makecache

然后重新运行bash openvpn-install.sh，选择3，remove VPN。然后重新运行bash openvpn-install.sh，一路回车即可。



####配置启动mysql

service mysqld start

mysql -uroot < /openvpn/static/openvpn.sql



###安装Python3.6.5
cd /openvpn/ 

wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz


tar xzvf Python-3.6.5.tgz

rm -rf /openvpn/Python-3.6.5/Modules/Setup.dist

cp -f /openvpn/Setup.dist /openvpn/Python-3.6.5/Modules/Setup.dist

cd /openvpn/Python-3.6.5/

./configure --prefix=/usr/local/python

make && make install

ln -s /usr/local/python/bin/python3.6 /usr/bin/python3

ln -s /usr/local/python/bin/pip3.6 /usr/bin/pip3

yum install -y python-pip

pip3 install flask pymysql paramiko requests


##准备启动程序，清理垃圾文件

cd /openvpn/ 

rm -rf /openvpn/users/README

rm -rf /openvpn/Setup.dist

rm -rf Python-3.6.5*

rm -rf OpenVpnWithWebControl*

rm -rf master

chmod +x *



####启动程序

nohup python3 /openvpn/main.py > /openvpn/main.log 2>&1 &

#浏览器输入服务器IP即可访问管理后台。



###注意：

###默认管理员admin，密码admin

###默认邀请注册码openvpn

###请登入系统后尽快修改管理员密码以及注册码。

