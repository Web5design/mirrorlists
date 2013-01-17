#!/bin/bash

set -e

LOGFILE=/var/log/gunicorn/login.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=1
USER=www-data
GROUP=www-data
ADDRESS=127.0.0.1:8001
#ADDRESS=0.0.0.0:8000
#test -d $LOGDIR || mkdir -p $LOGDIR
#cd /root/.virtualenvs/ldap && source bin/activate
cd /var/www/mirrorlists/
exec /usr/bin/uwsgi_python27 -s 127.0.0.1:3031 --uid www-data --gid www-data --module mirrorlists --callable app 

