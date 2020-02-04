export PYTHONPATH=../
celery -A scheduler.celery worker -E -B --loglevel=INFO