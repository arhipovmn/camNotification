#!/usr/bin/env bash
BASE=$(cd $(dirname $BASH_SOURCE) && pwd)
cd $BASE

PID=$BASE/temp/main.pid

_start() {
    set -e
    source $BASE/venv/bin/activate
    python $BASE/main.py & echo $! > $BASE/temp/main.pid
    echo "done"
}

start() {
    echo "==== Start"

    if [ -f $PID ]
    then
        if [ -z "$(ps -p $( cat $PID ) | grep $( cat $PID ) | grep -v "grep")" ]; then
            _start
        else
            echo "main.py already started?"
        fi;
    else
        _start
    fi
}

stop() {
    echo "==== Stop"

    if [ -f $PID ]
    then
        if kill $( cat $PID )
        then echo "done"
        fi
        /bin/rm -f $PID
    else
        echo "no pid file. already stopped?"
    fi
}

status() {
    echo "==== Status"

    if [ -f $PID ]
    then
        echo
        echo "Pid file: $( cat $PID ) [$PID]"
        echo
        ps -ef | grep -v grep | grep $( cat $PID )
    else
        echo
        echo "No Pid file"
    fi
}


case "$1" in
    'start')
            start
            ;;
    'stop')
            stop
            ;;
    'restart')
            stop
            echo "..."
            sleep 1
            start
            ;;
    'status')
            status
            ;;
    *)
            echo
            echo "usage: $0 { start | stop | restart | status }"
            echo
            exit 1
            ;;
esac

exit 0
