from flask import Blueprint
from flaskr.api.celery_task import add
bp = Blueprint('back', __name__)


@bp.route('/test')
def back():
    task = add.delay(10, 20)
    print(task.ready())
    return 'task_progress'
