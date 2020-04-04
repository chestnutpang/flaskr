# from flaskr.mysqldb import DbBase
# from sqlalchemy import Column, String, Integer, ForeignKey, VARCHAR
from flaskr.database import DbBase, db


class Blog(DbBase):
    __tablename__ = 'Blog'
    title = db.Column(db.VARCHAR(20), nullable=False)
    content = db.Column(db.VARCHAR(500), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.author_id = user_id
