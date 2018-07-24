# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/31 17:47
# @Author  : lemon

from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp,ValidationError

from app.libs.enums import ClientTypeNum
from app.models.user import User
from app.libs.base_form import BaseForm as Form


class ClientForm(Form):
    '''
        ClientForm的校验，是非常有必要的。继承这个类，可少写type校验的重复代码。
    '''
    account = StringField(validators=[DataRequired(message='账号不能为空'),length(
        min=5,max=32
    )])
    secret = StringField()
    type   = IntegerField(validators=[DataRequired()])

    def validate_type(self,value):
        try:
            client = ClientTypeNum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client




class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='邮箱不合法')])
    secret = StringField(validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='密码不合法,请输入6至22位密码')])
    nickname = StringField(validators=[
        DataRequired(),
        length(min=2, max=22)])

    def validate_account(self,value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_nickname(self,value):
        if User.query.filter_by(nickname=value.data).first():
            raise ValidationError('该昵称已注册')

class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])