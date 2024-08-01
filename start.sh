sh stop.sh
nohup python3 -m gunicorn -c soulbook/config/gunicorn.py --worker-class sanic.worker.GunicornWorker soulbook.server:app --log-level=debug >/dev/null 2>&1 &
