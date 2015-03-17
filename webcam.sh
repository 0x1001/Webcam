#!/bin/bash
#
#  Starts Web Camera software
#

CMD=$1
COMP=$2

if [ "$CMD" == "" ]; then
    echo "Usage:"
    echo "$0 start     - to start both Web page and camera application"
    echo "$0 stop      - to stop both Web page and camera application"
    echo "$0 start app - to start only camera application"
    echo "$0 start web - to start only web application"

    exit 0
fi

cd $(dirname "${BASH_SOURCE[0]}")

function wait_for_pid {
    pid=$1
    while [ true ]; do
        if [ -z "$(ps -A|grep python|grep $pid)" ]; then
            break
        fi
        sleep 0.2
    done
}

function start_app {
    if [ -f app.pid ]; then
        pid=$(cat app.pid)

        if [ -n "$(ps -A|grep python|grep $pid)" ]; then
            echo "It is already running! PID: $pid"
            exit 1
        fi
    fi

    date >> app.log
    python app/app.py >> app.log 2>&1 &
    echo $! > app.pid
}

function stat_web {
    if [ -f web.pid ]; then
        pid=$(cat web.pid)

        if [ -n "$(ps -A|grep python|grep $pid)" ]; then
            echo "It is already running! PID: $pid"
            exit 1
        fi
    fi

    python web/manage.py runserver 0.0.0.0:80 > web.log 2>&1 &
    echo $! > web.pid
}

function stop_app {
    if [ ! -f app.pid ]; then
        echo "Notihng to stop. It is not running!"
        exit 1
    fi
    pid=$(cat app.pid)
    kill -INT $pid
    wait_for_pid $pid
    rm app.pid
}

function stop_web {
    if [ ! -f web.pid ]; then
        echo "Notihng to stop. It is not running!"
        exit 1
    fi
    pid=$(cat web.pid)
    pkill -TERM -P $pid
    wait_for_pid $pid
    rm web.pid
}

if [ "$CMD" == "start" ]; then
    if [ "$COMP" == "" ]; then
        start_app
        stat_web
    elif [ "$COMP" == "app" ]; then
        start_app
    elif [ "$COMP" == "web" ]; then
        stat_web
    else
        echo "Wrong application!"
        exit 1
    fi

elif [ "$CMD" == "stop" ]; then
    if [ "$COMP" == "" ]; then
        stop_app
        stop_web
    elif [ "$COMP" == "app" ]; then
        stop_app
    elif [ "$COMP" == "web" ]; then
        stop_web
    else
        echo "Wrong application!"
        exit 1
    fi
fi
