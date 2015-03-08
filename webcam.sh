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

function start_app {
    date >> app.log
    python app/app.py >> app.log 2>&1 &
    echo $! > app.pid
}

function stat_web {
    python web/manage.py runserver [::]:80 > web.log 2>&1 &
    echo $! > web.pid
}

function stop_app {
    pid=`cat app.pid`
    kill -INT $pid
    rm app.pid
}

function stop_web {
    pid=`cat web.pid`
    pkill -TERM -P $pid
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
