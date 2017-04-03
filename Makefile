.PHONY: client server build celery

server:
	gunicorn server:app -c gunicorn.conf.py

celery:
	celery -A server.celery worker

client:
	python client.py

build:
	pip install -r requirements.txt
