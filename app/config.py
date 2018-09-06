# -*- coding: utf-8 -*-
# @Time    : 2018/9/6 16:48
# @Author  : Zhang
# @FileName: config.py.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
import os
import pymysql
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:0304@localhost/blog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False