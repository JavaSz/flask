# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 21:41
# @Author  : Zhang
# @FileName: Restful_api.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
import views
from flask.ext import restful


api = restful.Api(views.app)


class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/api/token')

