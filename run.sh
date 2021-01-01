#!/bin/sh
DIRNAME=`dirname $0`

python3 "${DIRNAME}/dos/app.py" &

python3 "${DIRNAME}/monitor/app.py" &

nginx

while true
do
     pgrep -f "dos/app.py" 1>/dev/null 2>/dev/null || exit 1
     pgrep -f "monitor/app.py" 1>/dev/null 2>/dev/null || exit 2
     pgrep "nginx" 1>/dev/null 2>/dev/null || exit 3
done
