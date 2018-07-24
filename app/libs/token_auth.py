# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/6/5 17:02
# @Author  : lemon
from collections import namedtuple

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired
from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth

from app.libs.exception import AuthFailedException, ForbiddenException
from app.libs.scope import is_in_scope

auth = HTTPBasicAuth()

Account_User = namedtuple('Account_User',['uid','account_type','scope'])

@auth.verify_password
def verify_password(token,password=None):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailedException(msg='token is invalid',
                                  error_code=1002)
    except SignatureExpired:
        raise AuthFailedException(msg='token is expired',
                                  error_code=1003)
    uid = data['uid']
    account_type = data['type']
    scope = data['scope']

    allow = is_in_scope(scope,request.endpoint)
    if not allow:
        raise ForbiddenException()
    return Account_User(uid,account_type,scope)





