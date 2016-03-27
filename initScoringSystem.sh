#!/bin/bash

LOGFILE="stdout_run.log"


start(){
    echo 'Starting Scoring System ...'
    gunicorn --bind 0.0.0.0:8090 \
        --worker-connections=2 \
        --error-logfile='errors.log' \
        --pid run.pid --daemon run >> $LOGFILE 2>&1 &
}

stop(){
    echo 'Stopping Scoring System ...'
    if [ -e "run.pid" ]; then
        kill -TERM $(cat "run.pid")
        rm "run.pid"
    fi
}

case "$1" in
    start)
        start
    ;;
    stop)
        stop
    ;;
    restart)
        stop
        start
    ;;
    *)
    echo $"Usage: $0 {start|stop|restart}"
    exit 1
esac