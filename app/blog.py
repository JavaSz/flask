# -*- coding: utf-8 -*-
# @Time    : 2018/9/6 18:35
# @Author  : Zhang
# @FileName: blog.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
from app import app


def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)

# 请记住，flask命令依赖于FLASK_APP环境变量来知道Flask应用入口在哪里。
# 对于本应用，正如第一章，你需要设置(windows/set FLASK_APP = blog.py。
# linux export FLASK_APP=blog.py
