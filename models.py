# -*- coding: utf-8 -*-
# @Time    : 2018/9/3 18:03
# @Author  : Zhang
# @FileName: models.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
from views import db
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
engine = create_engine("mysql+pymysql://root:0304,@127.0.0.1/flaskr", max_overflow=5)
Base = declarative_base()
# Session.configure(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    passwd = Column(String(128))
    is_admin = Column(Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


# drop_db()
init_db()