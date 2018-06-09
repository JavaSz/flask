# -*- coding: utf-8 -*-
# @Time    : 2018/6/9 21:00
# @Author  : Zhang
# @FileName: one.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)


class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)