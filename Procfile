web : flask db upgrade; gunicorn blog:app_instance
worker: rq worker -u $REDIS_URL first-worker