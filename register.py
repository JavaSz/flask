# -*- coding: utf-8 -*-
# @Time    : 2018/7/12 11:16
# @Author  : Zhang
# @FileName: auth.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',
    passwd='0304',
    db='flaskr',
    charset='utf8'
)
g = db.cursor()

