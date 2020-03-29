from flask import Blueprint
# from celery.bootsteps import Blueprint
from flaskr.api import celery_task

bp = Blueprint('back', __name__)


@bp.route('/back')
def back():
    task = celery_task.add.delay(10, 20)
    print(task.ready())
    return 'task_progress'


