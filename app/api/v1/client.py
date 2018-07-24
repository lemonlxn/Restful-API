# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/31 17:43
# @Author  : lemon
from flask import request


from app.libs.enums import ClientTypeNum
from app.libs.exception import Success
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm

api = Redprint('client')

# 类似总分关系

@api.route('/register',methods=['POST'])
def create_client():

    form = ClientForm().validate_parameter_for_api()
    promise = {
        ClientTypeNum.USER_EMAIL:__register_user_by_email
    }
    promise[form.type.data]()

    return Success()

def __register_user_by_email():
    email_form = UserEmailForm().validate_parameter_for_api()

    with db.auto_commit():
        user =User()
        user.nickname = email_form.nickname.data
        user.email = email_form.account.data
        user.password = email_form.secret.data
        db.session.add(user)
