# -*- coding: utf-8 -*-
# @Time    : 2018/4/10 19:48
# @Author  : Zhang
# @FileName: flaskr.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
# 导入所有的模块
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing


# sql配置文件
DATABASE = 'C:\\Users\\Administrator\\PycharmProjects\\PythonProject\\week2\\Flask2\\temp\\flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'


# 创建应用
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# 初始化sql
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('C:\\Users\\Administrator\\PycharmProjects\\PythonProject\\week2\\Flask2\\schema.sql') as f:
            db.cursor().executescript(f.read().decode())
        # 提交到数据库执行
        db.commit()


# connect database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


# 定义全局变量g.db
@app.before_request
def before_request():
    g.db = connect_db()


@app.route('/post/<int:id>')
def get_post(id):
    cur = g.db.execute('select content from entries where id = id')
    entries = [dict(id=row[0]) for row in cur.fetchall()]
    return render_template('archive.html', entries=entries)


@app.route('/useful_links')
def show_friends():
    return render_template('links.html')


@app.route('/about')
def show_about():
    return render_template('about.html')


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, description, date, author from entries order by id desc')
    entries = [dict(title=row[0], description=row[1], date=row[2], author=row[3]) for row in cur.fetchall()]
    return render_template('index.html', entries=entries)


# 1. g对象是专门用来保存用户的数据的。
# 2. g对象在一次请求中的所有的代码的地方，都是可以使用的
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, description, content, date, author, tags) values (?, ?, ?, ?, ?, ?)', [
        request.form['title'],
        request.form['description'],
        request.form['content'],
        request.form['date'],
        request.form['author'],
        request.form['tags']
                                                                                                         ])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# Markdown
@app.route('/test1')
def test_1():
    mkd = '''
    # header
    ## header2
    [picture](http://www.example.com)
    * 1
    * 2
    * 3
    **bold**
    '''

    return render_template('test1.html', mkd=mkd)


if __name__ == '__main__':
    app.run(port=80)
    # show_entries()
    get_archives()
