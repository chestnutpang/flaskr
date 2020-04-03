# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy import Column, String, Integer, VARCHAR
# from flaskr.mysqldb import DbBase, DatabaseConnect
from flaskr.database import DbBase, db
from flask import g


class User(DbBase):
    __tablename__ = 'User'
    username = db.Column(db.VARCHAR(12), nullable=False)
    password = db.Column(db.VARCHAR(12), nullable=False)
    # blog = db.relationship('Blog')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def login(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user is None:
            raise ValueError
        if user.password != password:
            raise ValueError
        g.user = user.id
        return user

    @classmethod
    def check_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()
