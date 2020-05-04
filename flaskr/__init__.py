import os
from flask import Flask
from flaskr.database import init_db
from flaskr.config import Config
from flaskr.handle_helper import *
from gevent.pywsgi import WSGIServer
import logging
import sys


class Server:
    app = Flask(__name__, instance_relative_config=True)

    @classmethod
    def init_app(cls, test_config=None):
        # from . import db
        from flaskr.celery_app import cele
        cls._log_init(log_level=config.Config.log_level)
        cls.app.config.from_object(Config)
        cls._register_bluepring(cls.app)
        try:
            os.makedirs(cls.app.instance_path)
        except OSError:
            pass
        
        cls.app.before_request(before_request)
        cls.app.after_request(after_request)
        # app.errorhandler(Exception)(error_handle)
        cls._init_ext(cls.app)
        return cls.app

    @classmethod
    def run(cls):
        logging.info(f'listen at {config.Config.ip}:{config.Config.port}')
        if config.Config.use_ssl is False:
            server = WSGIServer((config.Config.ip, config.Config.port), cls.app, log=None)
        else:
            server = WSGIServer((config.Config.ip, config.Config.port), cls.app, log=None, 
                                keyfile=config.Config.key_file, certfile=config.Config.cert_file)
        logging.info('============ server start ============')
        server.serve_forever()


    @staticmethod
    def _register_bluepring(app):
        from flaskr.api import user, bill, blog, back
        app.register_blueprint(user.bp)
        app.register_blueprint(blog.bp, url_prefix='/blog')
        app.register_blueprint(back.bp, url_prefix='/back')
        app.register_blueprint(bill.bp, url_prefix='/bill')
        @app.route('/hello')
        def hello():
            return 'Hello World!'
        app.route('/')(blog.index)

    @staticmethod
    def _init_ext(app):
        from flaskr.redisutils import RedisConn
        init_db(app)
        RedisConn.init(config.Config.REDIS_HOST, config.Config.REDIS_PORT,
                       config.Config.REDIS_PASSWORD, config.Config.REDIS_DB)

    @staticmethod
    def _log_init(log_level='DEBUG', log_path='', log_reserve='', log_to_console=''):
        # SvrTool.ensure_path(log_path)
        #
        # file_handler = RotatingHandler(
        #     filename=os.path.join(log_path, SvrTool.get_process_name() + '.log'), when='H',
        #     backupCount=log_reserve, encoding='utf-8', delay=True)
        # if log_to_console:
        #     stream_heandler = logging.StreamHandler(stream=sys.stdout)
        #     _handlers = (file_handler, stream_heandler)
        # else:
        #     _handlers = (file_handler,)

        logging.basicConfig(
            level=log_level,
            # handlers=_handlers,
            format='%(asctime)s[%(levelname)s]|%(name)s|%(process)d|%(threadName)s|'
                   '%(module)s:%(lineno)d(%(funcName)s)|%(message)s')

        logging.getLogger('chardet.charsetprober').setLevel(logging.WARNING)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
