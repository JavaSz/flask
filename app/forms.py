# -*- coding: utf-8 -*-
# @Time    : 2018/9/2 17:46
# @Author  : Zhang
# @FileName: forms.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


# User login form
class LoginForm(FlaskForm):
    # 它会要求用户输入username和password，并提供一个“remember me”的复选框和提交按钮
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# User Register
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])  # 验证是否为邮箱格式 Email()
    about_me = StringField('AboutMe', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')  # EqualTo的验证器，它将确保其值与第一个password字段的值相同

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('AboutMe', validators=[Length(min=0, max=30)])
    submit = SubmitField('Submit')


    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')