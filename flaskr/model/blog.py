from flaskr.mysqldb import DbBase
from sqlalchemy import Column, String, Integer, ForeignKey


class Blog(DbBase):
    __tablename__ = 'user'

    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(String(20), ForeignKey('user.id'))

    def __init__(self, title, content):
        self.title = title
        self.content = content
