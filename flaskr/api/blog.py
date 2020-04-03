from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

# from flaskr.db import get_db
from flaskr.model import *
from flaskr import comm

bp = Blueprint('blog', __name__)


@bp.route('/', methods=['GET'])
def index():
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    posts = []
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


# 更新或删除时获取 blog 的对象
def get_post(_id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (_id,)
    ).fetchone()

    if post is None:
        abort(404, f'Post id {_id} doesn\'t exist.')
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:_id>/update', methods=['GET', 'POST'])
# @comm.login_required
def update(_id):
    post = get_post(_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, _id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)


@bp.route('/<int:_id>/delete', methods=['POST'])
# @comm.login_required
def delete(_id):
    get_post(_id)
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id = ?', (_id, )
    )
    db.commit()
    return redirect(url_for('blog.index'))
