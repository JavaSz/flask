# -*- coding: utf-8 -*-
# @Time    : 2018/9/3 18:03
# @Author  : Zhang
# @FileName: models.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
from flask_login import UserMixin
from app import db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# connect = create_engine("mysql+pymysql://root:0304@localhost:3306/flaskr",
#                         encoding="utf-8",
#                         echo=True)  # 连接数据库，echo=True =>把所有的信息都打印出来


Base = declarative_base()  # 生成ORM基类


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # 我不需要为timestamp字段设置一个值，因为这个字段有一个默认值，你可以在模型定义中看到。
    # 那么user_id字段呢？ 回想一下，我在User类中创建的db.relationship为用户添加了posts属性，
    # 并为用户动态添加了author属性。 我使用author虚拟字段来调用其作者，
    # 而不必通过用户ID来处理。 SQLAlchemy在这方面非常出色，因为它提供了对关系和外键的高级抽象。
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# Base.metadata.create_all(connect)  # 创建表结构
