from celery import Celery
from flaskr.config import flaskConfig


celery_app = Celery(
    'flask_Celery',
    broker=flaskConfig.CELERY_BROKER_URL,
    backend=flaskConfig.CELERY_RESULT_BACKEND,
    include=['flaskr.celery_app.celery_task.add']
)


