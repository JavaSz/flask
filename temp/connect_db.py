# -*- coding: utf-8 -*-
# @Time    : 2018/4/11 14:14
# @Author  : Zhang
# @FileName: connect_db.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
import sqlite3

conn = sqlite3.connect('flask.db')
c = conn.cursor()
c.execute('''CREATE TABLE COMPANY
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);''')
print("Table created successfully")
conn.commit()
conn.close()
