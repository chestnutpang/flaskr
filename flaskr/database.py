from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    # db.drop_all(app=app)
    db.create_all(app=app)


class DbBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    createdAt = db.Column(db.DateTime, default=datetime.now())
    updatedAt = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def save(self):
        print(db.session)
        db.session.add(self)
        db.session.commit()

    @classmethod
    def save_all(cls, data_list):
        db.session.add_all(data_list)
        db.session.commit()

    @property
    def _id(self):
        return self.id
