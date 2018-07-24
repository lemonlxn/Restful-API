# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/28 21:40
# @Author  : lemon

from flask import Blueprint

from app.api.v1 import book,user,client,token,gift

def create_blueprint_v1():
    bp_v1 = Blueprint('v1',__name__)


    book.api.register(bp_v1)
    user.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    gift.api.register(bp_v1)

    return bp_v1

