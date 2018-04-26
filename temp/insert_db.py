# -*- coding: utf-8 -*-
# @Time    : 2018/4/11 14:23
# @Author  : Zhang
# @FileName: insert_db.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
import sqlite3

conn = sqlite3.connect('flask.db')
c = conn.cursor()
print("Opened database successfully")

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )");

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");

conn.commit()
print("Insert successfully")
conn.close()
