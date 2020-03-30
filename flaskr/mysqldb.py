from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
import uuid


Base = declarative_base()


class DatabaseConnect:
    session = None

    @classmethod
    def init(cls, user, password, port, db):
        uri = f'mysql_pymysql://{user}:{password}:{port}/{db}'
        engine = create_engine(uri)
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind=engine)
        cls.session = DBSession()


    @classmethod
    def get_session(cls):
        if cls.session is None:
            raise ValueError
        return cls.session


class DbBase(Base):
    id = Column(String, default=uuid.uuid4().hex, primary_key=True)
    _createdAt = Column(DateTime, default=datetime.now())
    _updatedAt = Column(DateTime, default=datetime.now())

    def save(self):
        session = DatabaseConnect.get_session()
        session.add(self)
        session.commit()
