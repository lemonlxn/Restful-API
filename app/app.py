# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/28 21:35
# @Author  : lemon
from datetime import date

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.exception import ServerException


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o,'keys') and hasattr(o,'__getitem__'):
            return dict(o)
        if isinstance(o,date):
            return o.strftime('%Y-%m-%d')
        raise ServerException()


class Flask(_Flask):
    json_encoder = JSONEncoder


