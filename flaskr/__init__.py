import os
from flask import Flask
from celery import Celery


def create_app(test_config=None):
    from . import db
    from . import auth
    from . import blog

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        CELERY_BROKER_URL='redis://loaclhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    )
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    @app.route('/hello')
    def hello():
        return 'Hello World!'

    return app

