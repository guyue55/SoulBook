#!/usr/bin/env bash
ps -ef | grep "gunicorn -c config/gunicorn.py --worker-class sanic.worker.GunicornWorker server:app" | grep -v grep | awk '{print $2}' | xargs kill -9
nohup gunicorn -c config/gunicorn.py --worker-class sanic.worker.GunicornWorker server:app >/dev/null &2>1 &
