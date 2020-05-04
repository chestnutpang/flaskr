

class Config:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/flaskr'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'ASDFEWA'

    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None
    REDIS_DB = 0

    use_ssl = False
    ip = '0.0.0.0'
    port = 5000
    key_file = ''
    cert_file = ''
