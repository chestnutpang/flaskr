from celery import Celery
from flaskr.config import Config


celery_app = Celery(
    'flask_Celery',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
    include=['flaskr.celery_app.celery_task']
)
