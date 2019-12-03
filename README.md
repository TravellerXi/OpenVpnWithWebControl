# OpenVpnWithWebControl
OpenVpnWithWebControl

###本软件提供web界面的OPENVPN，以下是安装本软件方法：

###必读：
#环境：Centos 6.5
#Python 3，在下述安装中，使用Python3.6.5，其他Python3版本亦可。（也就是说如果安装了Python3，您可以跳过Python3，安装，只需执行pip3 install flask pymysql paramiko requests）
#数据库采用Mysql，默认开启用户openvpn，密码openvpn，建立数据库openvpn。

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

###在COMMIT前一行加一句：

-A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT
####

service iptables restart

cd /openvpn
wget https://codeload.github.com/TravellerXi/OpenVpnWithWebControl/zip/master
unzip master
\cp -R -f OpenVpnWithWebControl-master/* /openvpn/

Error: Cannot retrieve metalink for repository: epel. Please verify its path and try again  /etc/yum.repos.d/epel.repo
mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=epel-6&arch=$basearch (改为http)
yum clean all && yum makecache

####配置启动mysql
service mysql start
mysql -uroot < /openvpn/openvpn.sql


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
#浏览器输入本机IP即可访问管理后台。


###注意：
###默认管理员admin，密码admin
###默认邀请注册码openvpn。
###请登入系统后尽快修改管理员密码以及注册码。
