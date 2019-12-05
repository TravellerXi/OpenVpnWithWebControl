#!/bin/bash
nohup python3 /openvpn/main.py > /openvpn/main.log 2>&1 & echo $! > /openvpn/process.pid &
