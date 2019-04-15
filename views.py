# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 20:33
# @Author  : Zhang
# @FileName: views.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import numpy as np
import pymysql
from app.config import Config
# 创建应用
# ... add more variables here as needed
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = '0304'
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


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


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


# @app.route('/archives/<date>')
# def time_get_post(date):
#     cur = g
#     g.execute("select * from entries where date= {}".format(date))
#     archives = cur.fetchall()
#     archive = np.array(archives)
#     # 文章是否存在
#     if np.any(archive):
#         return render_template('index.html', archive=archive)
#     else:
#         return render_template('404.html')


@app.route('/useful_links')
def show_friends():
    return render_template('links.html')


@app.route('/about')
def show_about():
    return render_template('about.html')


@app.route('/')
def show_entries():
    # get_recent_posts()
    cur = g
    g.execute('select id, title, description, date, author, tags from entries order by id desc')
    entries = [dict(id=row[0], title=row[1], description=row[2], date=row[3], author=row[4], tags=row[5]) for row in cur.fetchall()]
    g.execute('select * from entries order by date desc LIMIT 0,2')
    posts = [dict(id=row[0], title=row[1], description=row[2], date=row[3], author=row[4]) for row in cur.fetchall()]
    return render_template('index.html', entries=entries, posts=posts)


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
        if request.form['username'] != app.config['ADMIN_USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['ADMIN_PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    # form = LoginForm()
    # # form.validate_on_submit()实例方法会执行form校验的工作
    # if form.validate_on_submit():
    #     flash('Login requested for user {}, remember_me={}'.format(
    #         form.username.data, form.remember_me.data))
    #     return redirect('/')
    return render_template('login.html', error=error)


@app.route('/admin/edit')
def show_edit():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            render_template('editor.html')
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/register')
def register():
    return render_template('app/templates/register.html')