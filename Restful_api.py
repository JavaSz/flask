# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 21:41
# @Author  : Zhang
# @FileName: Restful_api.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
import views
from flask.ext import restful
import json

g = views.g
api = restful.Api(views.app)


class GetPosts(restful.Resource):
    def get(self):

        all_infos = []
        cur = g
        g.execute('select id, title, description, date, author, tags from entries order by id desc')
        infos = [dict(id=row[0], title=row[1], description=row[2], date=row[3], author=row[4], tags=row[5]) for row in cur.fetchall()]
        for info in infos:
            d = {
                'id': info.id,
                'title': info.title,
                'description': info.description,
                'date': info.date,
                'author': info.author,
                'tags': info.tags
            }
            all_infos.append(d)
            print(all_list=all_infos)
        return json(all_infos)


api.add_resource(GetPosts, '/api/token')

