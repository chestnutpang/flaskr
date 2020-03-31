from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
Base = declarative_base()


class DatabaseConnect:
    session = None

    @classmethod
    def init(cls, user, password, host, port, db):
        uri = f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'
        engine = create_engine(uri)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind=engine)
        cls.session = DBSession()


    @classmethod
    def get_session(cls):
        if cls.session is None:
            raise ValueError
        return cls.session


class DbBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now())

    def save(self):
        session = DatabaseConnect.get_session()
        session.add(self)
        session.commit()
