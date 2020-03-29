from flaskr.cele import celery_app


@celery_app.task(name='')
def add(arg1, arg2):
    return arg1 + arg2
