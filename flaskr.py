# -*- coding: utf-8 -*-
# @Time    : 2018/4/10 19:48
# @Author  : Zhang
# @FileName: flaskr.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
# 导入所有的模块
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import numpy as np
import pymysql


# 创建应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = '12345'
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# connect database
db = pymysql.connect(
    host='localhost',
    user='root',
    passwd='0304',
    db='flaskr',
    charset='utf8'
)
g = db.cursor()

# 关闭数据库


@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('editor.html')


@app.route('/post/<post_id>')
def get_post(post_id):
    cur = g
    g.execute("select * from entries where id= {}".format(post_id))
    # entries = [dict(id=row[0]) for row in cur.fetchall()]
    item1 = cur.fetchone()
    item = np.array(item1)
    # 文章是否存在
    if np.any(item):
        return render_template('archive.html', item=item)
    else:
        return render_template('404.html')


@app.route('/useful_links')
def show_friends():
    return render_template('links.html')


@app.route('/about')
def show_about():
    return render_template('about.html')


@app.route('/')
def show_entries():
    cur = g
    g.execute('select id, title, description, date, author from entries order by id desc')
    entries = [dict(id=row[0], title=row[1], description=row[2], date=row[3], author=row[4]) for row in cur.fetchall()]
    return render_template('index.html', entries=entries)


def show_tags():
    cur = g
    g.execute('select tags from entries')
    for row in cur.fetchall():
        print(row)
    return row

# 1. g对象是专门用来保存用户的数据的。
# 2. g对象在一次请求中的所有的代码的地方，都是可以使用的
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.execute('insert into entries (title, description, content, date, author, tags) values (%s, %s, %s, %s, %s, %s)', [
        request.form['title'],
        request.form['description'],
        request.form['content'],
        request.form['date'],
        request.form['author'],
        request.form['tags']
                                                                                                         ])
    db.commit()
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


if __name__ == '__main__':
    app.run(port=23333)
    # get_post()

