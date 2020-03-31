from functools import wraps


def login_required(func):

    @wraps
    def wrapper(*args, **kwargs):
        return

    return wrapper
