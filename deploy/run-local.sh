export PYTHONPATH=../server
celery -A server.scheduler.celery worker -E -B --loglevel=INFO