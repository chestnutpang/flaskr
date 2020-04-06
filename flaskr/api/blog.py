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
    blog_list = Blog.query.join(User, User.id == Blog.author_id).all()
    return render_template('blog/index.html', posts=blog_list)


@bp.route('/create', methods=['GET', 'POST'])
@comm.login_required
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
            # db.execute(
            #     'INSERT INTO post (title, body, author_id)'
            #     ' VALUES (?, ?, ?)',
            #     (title, body, g.user['id'])
            # )
            # db.commit()
            print()
            new_blog = Blog(title, body, g.user._id)
            new_blog.save()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


# 更新或删除时获取 blog 的对象
def get_post(_id, check_author=True):

    # post = get_db().execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' WHERE p.id = ?',
    #     (_id,)
    # ).fetchone()
    blog = Blog.query.join(User, User.id == Blog.author_id).filter(Blog.id == _id).one()
    if blog is None:
        abort(404, f'Post id {_id} doesn\'t exist.')
    if check_author and blog.author_id != g.user.id:
        abort(403)

    return blog


@bp.route('/<int:_id>/update', methods=['GET', 'POST'])
@comm.login_required
def update(_id):
    blog = get_post(_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)

        else:
            # db = get_db()
            # db.execute(
            #     'UPDATE post SET title = ?, body = ?'
            #     ' WHERE id = ?',
            #     (title, body, _id)
            # )
            # db.commit()
            blog.title = title
            blog.content = body
            blog.save()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=blog)


@bp.route('/<int:_id>/content', methods=['GET'])
def content(_id):
    blog = Blog.query.filter(Blog.id == _id).one()
    return render_template('blog/content.html', post=blog)


@bp.route('/<int:_id>/delete', methods=['POST'])
@comm.login_required
def delete(_id):
    blog = get_post(_id)
    # db = get_db()
    # db.execute(
    #     'DELETE FROM post WHERE id = ?', (_id, )
    # )
    Blog.remove(blog)
    return redirect(url_for('blog.index'))
