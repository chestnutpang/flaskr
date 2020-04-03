from functools import wraps
from flask import session
from flaskr.model.user_model import User


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        print(user_id, '>>>user id')
        if User.check_id(user_id) is None:
            raise ValueError()
        resp = func(*args, **kwargs)
        return resp

    return wrapper
