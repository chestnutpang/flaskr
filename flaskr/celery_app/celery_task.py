from flaskr.celery_app.cele import celery_app


@celery_app.task(name='celery_task.add')
def add(arg1, arg2):
    return arg1 + arg2
