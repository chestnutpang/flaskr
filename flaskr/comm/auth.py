from functools import wraps
from flask import session
from flaskr.model.user_model import User
from flaskr.exception import NormalError
from flaskr.err_code import ErrorCode


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if User.check_id(user_id) is None:
            raise NormalError(*ErrorCode.LOGIN_REQUIRE)
        resp = func(*args, **kwargs)
        return resp

    return wrapper
