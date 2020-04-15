# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy import Column, String, Integer, VARCHAR
# from flaskr.mysqldb import DbBase, DatabaseConnect
from flaskr.database import DbBase, db
from flask import g
import random


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('User.id'))
)


class User(DbBase):
    __tablename__ = 'User'
    id = db.Column(db.Integer, unique=True, autoincrement=True, primary_key=True)
    username = db.Column(db.VARCHAR(12), nullable=False)
    password = db.Column(db.VARCHAR(12), nullable=False)
    avatar = db.Column(db.VARCHAR(256), default=None)
    nickname = db.Column(db.VARCHAR(20), nullable=False)
    blog = db.relationship('Blog', backref='user')

    # 用户的关注与粉丝都是 User 时，
    # sqlalchemy 无法区分主次
    # 需使用 primaryjoin 与 secondaryjoin 两个参数指定
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        lazy='dynamic',  # 延迟求值，这样才能用 filter_by 过滤函数
        backref=db.backref('followers', lazy='dynamic')
    )

    def __init__(self, username, password, nickname=None):
        self.username = username
        self.password = password
        if nickname is not None:
            self.nickname = nickname
        else:
            self.nickname = f'user_{random.randint(0, 10000)}'

    @classmethod
    def login(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user is None:
            return None
        if user.password != password:
            return None
        g.user = user.id
        return user

    @classmethod
    def check_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()
