#!/usr/bin/env bash
MYPWD=$(cd $(dirname $BASH_SOURCE) && pwd)
cd $MYPWD

if [ -z "$(ps -p $(cat $MYPWD/temp/main.pid) | grep $(cat $MYPWD/temp/main.pid) | grep -v "grep")" ]; then
    set -e
    source $MYPWD/venv/bin/activate
    python $MYPWD/main.py & echo $! > $MYPWD/temp/main.pid
else
    echo "main.py already started"
fi;
