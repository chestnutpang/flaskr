import redis


class RedisConn:
    _redis_conn = None

    @classmethod
    def init(cls, host, port, password, db):
        uri = f'redis://{password}@{host}:{port}/{db}' if password is not None else f'redis://@{host}:{port}/{db}'
        cls._redis_conn = redis.from_url(uri)

    @classmethod
    def get_redis_conn(cls):
        return cls._redis_conn
