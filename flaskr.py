# -*- coding: utf-8 -*-
# @Time    : 2018/4/10 19:48
# @Author  : Zhang
# @FileName: flaskr.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
# 导入所有的模块
import views


if __name__ == '__main__':
    views.app.run(port=23333, debug=True)

