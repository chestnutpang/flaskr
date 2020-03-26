import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    # open_resource 打开文件，路径是相对于 flaskr 的
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


# click command 定义 init-db 的命令行 用于调用 init_db 函数
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('initialized the database.')


# 在应用中注册 close_db 与 init_db_command
def init_app(app):
    # teardown_appcontext 告诉 flask 在返回响应后进行清理时调用此函数
    app.teardown_appcontext(close_db)
    # 添加一个新的可以与 flask 一起工作的命令
    app.cli.add_command(init_db_command)
