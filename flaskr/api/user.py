import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.model import *
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'username is required.'
        elif not password:
            error = 'password is required.'
        if error is None:
            user = User(username, password)
            user.save()
            return redirect(url_for('auth.login'))
        else:
            flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.login(username, password)
        if user is None:
            error = '账号或密码不正确'
        else:
            session.clear()
            session['user_id'] = user._id
            return redirect(url_for('blog.index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.check_id(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))


# # 验证登录态的装饰器
# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))
#         return view(**kwargs)
#     return wrapped_view


from flaskr import comm

@bp.route('/test_login', methods=['GET'])
@comm.login_required
def test_login():
    print(session)
    return 'yes'
