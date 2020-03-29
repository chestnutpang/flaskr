from flask import Blueprint
from flaskr.celery_app.celery_task import add
bp = Blueprint('back', __name__)


@bp.route('/test')
def back():
    task = add.delay(10, 20)
    print(task.ready())
    return 'task_progress'
