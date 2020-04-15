from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
# from flaskr.db import get_db
from flaskr.exception import NormalError
from flaskr.model import *
from flaskr import comm, ErrorCode
from flaskr.redisutils import RedisConn

bp = Blueprint('blog', __name__)


@bp.route('/', methods=['GET'])
def index():
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    user_id = session.get('user_id')
    if user_id is None:
        blog_list = Blog.query.all()
        return render_template('blog/index.html', posts=blog_list)
    else:
        blog_list = Blog.query.all()
        user = User.query.get(user_id)
        print(user, '>>>>>>>>>>>>>')
        return render_template('blog/index.html', posts=blog_list, user=user)


@bp.route('/home/<user_id>', methods=['GET'])
def home(user_id):
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    blog_list = Blog.query.join(User, user_id == Blog.author_id).all()
    user = User.query.get(user_id)
    return render_template('blog/index.html', posts=blog_list, user=user)


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
            new_blog = Blog(title, body, g.user._id)
            new_blog.save()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


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
    blog = Blog.query.filter(Blog.id == _id).join(User, User.id == Blog.author_id).one()
    conn = RedisConn.get_redis_conn()
    like = conn.scard(f'blog_{_id}')
    if like is None:
        # conn.set(f'blog_{_id}', 0)
        like = 0
    return render_template('blog/content.html', post=blog, like=like, user=blog.user)


@bp.route('/<int:_id>/like', methods=['POST'])
@comm.login_required
def click_like(_id):
    conn = RedisConn.get_redis_conn()
    user_id = g.user._id
    blog_key = f'blog_{_id}'
    exist = conn.sismember(blog_key, user_id)
    if exist:
        conn.srem(blog_key, user_id)
    else:
        conn.sadd(blog_key, user_id)
    return redirect(url_for('blog.content', _id=_id))


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
