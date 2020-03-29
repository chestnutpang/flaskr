import os
from flask import Flask
from celery import Celery


def create_app(test_config=None):
    from . import db
    from flaskr.api import auth
    from flaskr.api import blog
    from flaskr.api import back
    from . import cele

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        CELERY_BROKER_URL='redis://loaclhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    cele.init_celery(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(back.bp)

    @app.route('/hello')
    def hello():
        return 'Hello World!'

    return app

