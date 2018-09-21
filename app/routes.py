# -*- coding: utf-8 -*-
# @Time    : 2018/9/6 17:04
# @Author  : Zhang
# @FileName: routes.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
from flask import render_template, flash, redirect, url_for, session, abort
from app import app
from app import db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from flask import request
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
import pymysql
import numpy as np

# connect database
data = pymysql.connect(
    host='localhost',
    user='root',
    passwd='0304',
    db='blog',
    charset='utf8'
)
g = data.cursor()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        # return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/index')
def show_entries():
    # get_recent_posts()
    cur = g
    g.execute('select id, title, description, timestamp, user_id, tags from post order by id desc')
    entries = [dict(id=row[0], title=row[1], description=row[2], date=row[3], author=row[4], tags=row[5]) for row in cur.fetchall()]
    g.execute('select id, title, description, timestamp, user_id, tags from post order by timestamp desc LIMIT 0,2')
    posts = [dict(id=row[0], title=row[1], description=row[2], date=row[3], author=row[4]) for row in cur.fetchall()]
    return render_template('index.html', entries=entries, posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


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
    g.execute("select * from post where id= {}".format(post_id))
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


