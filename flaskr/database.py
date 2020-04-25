from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    # db.drop_all(app=app)
    db.create_all(app=app)


class DbBase(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, unique=True, autoincrement=True, primary_key=True)
    createdAt = db.Column(db.DateTime, default=datetime.now())
    updatedAt = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def remove(cls, obj):
        db.session.delete(obj)
        db.session.commit()


    @classmethod
    def save_all(cls, data_list):
        db.session.add_all(data_list)
        db.session.commit()

    def set(self, key, value):
        self.__setattr__(key, value)

    def get(self, key):
        return self.__getattribute__(key)

    @property
    def _id(self):
        return self.id

    @property
    def get_table_name(self):
        return self.__tablename__
