#!/usr/bin/env bash
# 第一行是说明使用的什么脚本语言，这里是 bash， 固定用法
# workdir 是一个路径，即先切换到这个目录下，然后启动服务 （启动命令： python app.py）。其实不切换应该也可以
workdir=/V2rayWithWebControl

# 启动函数，切换路径=》其实就是 python app.py 。 前面一段指明是哪个路径下的python， 后面是 app.py 的路径， & 表示以后台方式启动（这里还不是很了解）
daemon_start() {
    cd $workdir
    /usr/bin/python3 /V2rayWithWebControl/main.py &
    echo "Server started."
}

# 停止函数，思路就是我们要找到这个进程号，然后把它 kill 掉
# 进程号寻找： 即 ps -ef|grep 命令， grep 用来过滤，awk 用来将过滤结果进行整理。 像这个命令，过滤出来有很多列，但我们只要进程号那一列，所以就是 {print $2}， 表示进程号那一列
# BEGIN{ ORS="," } 表示以逗号分隔每个进程号， 不写默认换行符分隔。
# 输出其实是一个字符串， 把它变为数组，因为我要取出第一个将进程杀死。 arr=... 这句话就是将 pid 变量里的内容转换为数组，存入arr。
# 接下来就是取到 arr 第一个进程号， 使用 kill 命令杀死

daemon_stop() {
    pid=`ps -ef | grep 'python3 /V2rayWithWebControl/main.py' | awk 'BEGIN{ ORS="," }{ print $2 }'`
    arr=(`echo ${pid} | tr ',' ' '`)
    echo ${arr[1]}
    kill ${arr[1]}
    sleep 3
    echo "Server killed."
}

# $1 表示命令行交互输入的第一个参数。 我们使用 ./dev.sh start 来运行脚本启动服务（因为此脚本文件名称为 dev.sh）， start 位置上的变量就是传入的第一个位置上的参数，也可以变为 stop， restart
case "$1" in
  start)
    daemon_start
    ;;
  stop)
    daemon_stop
    ;;
  restart)
    daemon_stop
    daemon_start
    ;;
  *)
    echo "Usage: ./dev.sh {start|stop|restart}"
    exit 1
esac
exit 0
