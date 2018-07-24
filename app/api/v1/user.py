# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/28 21:39
# @Author  : lemon
from flask import jsonify, g

from app import db
from app.libs.exception import DeleteSuccess, AuthFailedException
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User

api = Redprint('user')



@api.route('/<int:uid>',methods=['GET'])
@auth.login_required
def super_get_user(uid):
    # 进入此视图函数前，已做权限验证
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('',methods=['GET'])
@auth.login_required
def get_user():
    uid = g.user.id
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('/<int:uid>',methods=['DELETE'])
@auth.login_required
def super_delete_user(uid):
    uid = uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()




@api.route('',methods=['DELETE'])
@auth.login_required
def delete_user():
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()

    return DeleteSuccess()

@api.route('',methods=['PUT'])
def update_user():
    return ''

