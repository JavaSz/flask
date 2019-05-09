# -*- coding: utf-8 -*-
# @Time    : 2018/9/6 16:51
# @Author  : Zhang
# @FileName: __init__.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
from flask import Flask
import app.config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

app = Flask(__name__)

app.config.from_object(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
moment = Moment(app)


from app import routes, models


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)