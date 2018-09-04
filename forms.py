# -*- coding: utf-8 -*-
# @Time    : 2018/9/2 17:46
# @Author  : Zhang
# @FileName: forms.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


# User login form
class LoginForm(FlaskForm):
    # 它会要求用户输入username和password，并提供一个“remember me”的复选框和提交按钮
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

