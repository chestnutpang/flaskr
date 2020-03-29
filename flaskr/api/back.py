from flask import Blueprint
# from celery.bootsteps import Blueprint
from flaskr.cele import get_celery

bp = Blueprint('back', __name__)

celery_task = get_celery()


@bp.route('/test')
def back():
    task = celery_task.add.delay(10, 20)
    print(task.ready())
    return 'task_progress'
