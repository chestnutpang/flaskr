from celery import Celery
celery_app = None
from logging import getLogger

log = getLogger('cele')


def init_celery(app):
    global celery_app
    celery_app = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    log.debug('init celery success')
    celery_app.conf.update(app.config)


def get_celery():
    return celery_app
