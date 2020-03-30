from sqlalchemy.orm import relationship

from flaskr.mysqldb import DbBase
from sqlalchemy import Column, String, Integer


class User(DbBase):
    __tablename__ = 'user'

    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    blog = relationship('Blog')

    def __init__(self, username, password):
        self.username = username
        self.password = password


if __name__ == '__main__':
    user = User('123', '123')
    user.save()
