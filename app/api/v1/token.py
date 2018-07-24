# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/6/5 09:27
# @Author  : lemon
import time

from flask import current_app, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from app.libs.enums import ClientTypeNum
from app.libs.exception import AuthFailedException, Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, TokenForm

api = Redprint('token')

@api.route('',methods=['POST'])
def get_token():
    form = ClientForm().validate_parameter_for_api()
    promise = {
        ClientTypeNum.USER_EMAIL:User.verify
    }
    identity = promise[form.type.data](form.account.data,
                                       form.secret.data)

    token = generate_auth_token(identity['uid'],
                               form.type.data,
                               identity['scope'],
                               current_app.config['TOKEN_EXPIRATION'])
    t = {'token':token.decode('ascii')}
    return jsonify(t),201



@api.route('/secret',methods = ['POST'])
def get_token_info():
    # 获取令牌信息
    form = TokenForm().validate_parameter_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(form.token.data,return_header=True)
    except BadSignature:
        raise AuthFailedException(msg='token is invalid',
                                  error_code=1002)
    except SignatureExpired:
        raise AuthFailedException(msg='token is expired',
                                  error_code=1003)

    create_time = time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(data[1]['iat']))
    expire_time = time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(data[1]['exp']))


    r = {
        'uid':data[0]['uid'],
        'type':data[0]['type'],
        'scope':data[0]['scope'],
        'create_at':create_time,
        'expire_in':expire_time
    }


    return jsonify(r)



def generate_auth_token(uid,account_type,scope=None,expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
    return s.dumps({'uid':uid,
                    'type':account_type.value,
                    'scope':scope
                    })


