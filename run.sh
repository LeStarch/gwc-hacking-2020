#/bin/sh
DIRNAME=`dirname $0`

python3 "${DIRNAME}/monitor/app.py" &
python3 "${DIRNAME}/dos/app.py" &

nginx
