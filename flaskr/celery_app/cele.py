from celery import Celery
from flaskr.config import Config


uri = f'redis://{Config.REDIS_PASSWORD}@{Config.REDIS_HOST}:{Config.REDIS_PORT}/{Config.REDIS_DB}' \
    if Config.REDIS_PASSWORD is not None else f'redis://@{Config.REDIS_HOST}:{Config.REDIS_PORT}/{Config.REDIS_DB}'

celery_app = Celery(
    'flask_Celery',
    broker=uri,
    backend=uri,
    include=['flaskr.celery_app.celery_task']
)
