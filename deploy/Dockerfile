FROM python:3.7

RUN apt-get -y update && \
    apt-get install -y redis-server

ADD ./deploy/redis.conf /etc/redis/redis.conf
ADD ./server /opt/server

RUN pip install -r /opt/server/requirements.txt && \
    touch /var/log/redis.log && \
    touch /var/log/celery.log

EXPOSE 8000

CMD redis-server --daemonize yes && \
    cd /opt/ && \
    export PYTHONPATH=/opt/server && \
    celery -A server.app.scheduler.celery worker -E -B --loglevel=INFO --detach --logfile="/var/log/celery.log" && \
    python -m server.app.app


