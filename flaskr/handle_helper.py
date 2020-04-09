from flaskr.err_code import ErrorCode
from flask import redirect, url_for


def before_request():
    pass


def after_request(response):
    return response


def error_handle(e):
    print(e)
    if e.code == ErrorCode.LOGIN_REQUIRE[0]:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('blog.index'))
