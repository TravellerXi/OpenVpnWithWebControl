#!/bin/bash
cd /V2rayWithWebControl/
nohup /usr/bin/python3 main.py > main.log 2>&1 & echo $! > /V2rayWithWebControl/process.pid &
