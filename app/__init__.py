# -*- coding: utf-8 -*-
# @Time    : 2018/9/6 16:51
# @Author  : Zhang
# @FileName: __init__.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models




