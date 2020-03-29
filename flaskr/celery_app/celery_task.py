from flaskr.celery_app.cele import celery_app


@celery_app.task
def add(arg1, arg2):
    return arg1 + arg2
