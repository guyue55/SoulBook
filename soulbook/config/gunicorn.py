# gunicorn config
# gunicorn -c config/gunicorn.py --worker-class sanic.worker.GunicornWorker server:app
import os

os.environ['MODE'] = 'PRO'

WORKERS = os.getenv('WORKERS', 5)
TIMEOUT = os.getenv('TIMEOUT', 60)
HOST = os.getenv('HOST', '0.0.0.0')
PORT = os.getenv('PORT', 8001)

bind = f'{HOST}:{PORT}'
backlog = 2048

workers = WORKERS
worker_connections = 1000
keepalive = os.getenv('KEEPALIVE', workers)

spew = False
daemon = False
umask = 0
timeout = TIMEOUT
preload = True
