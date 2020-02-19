build_app:
	docker build -t food-grep-server -f ./deploy/Dockerfile .

run_local_dependecies:
	export PYTHONPATH=./server
	docker pull redis
	docker run -p "6379:6379" -d redis
	celery -A server.app.scheduler.celery worker -E -B --loglevel=INFO

run_local:
	export PYTHONPATH=./server
	python -m server.app.app

run_container:
	docker run -it -p "8000:8000" food-grep-server
