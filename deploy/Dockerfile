FROM python:3.7

RUN apt-get -y update && \
    apt-get install -y redis-server

ADD ./deploy/redis.conf /etc/redis/redis.conf
ADD ./server/app /opt/server-app/
ADD ./server/config /opt/config/

EXPOSE 8000

CMD redis-server --daemonize yes

