#################################################
# Gunicorn config for server
#################################################

bind = '0.0.0.0:8888'

# configure number of gunicorn workers
import multiprocessing
workers = multiprocessing.cpu_count() * 2 + 1

worker_class = 'gevent'

# dont daemonize; running inside docker
daemon = False
timeout = 60
pidfile = '/tmp/gunicorn.pid'

# error log to STDERR
errorlog = '-'
loglevel = 'info'

# access logs to STDERR also
accesslog = '-'
access_log_format = '%(h)s %(u)s [%(t)s] "%(m)s %(U)s %(H)s" %(s)s %(B)s %(T)s "%(f)s" "%(a)s" server'
