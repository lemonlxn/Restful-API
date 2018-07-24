# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/6/7 20:52
# @Author  : lemon

from app import create_app
from app.models.base import db
from app.models.user import User

app = create_app()

with app.app_context():
    with db.auto_commit():
        # 创建一个超级管理员
        user = User()
        user.nickname = 'Super'
        user.email = '999@qq.com'
        user.password = 'admin123'
        user.auth = 2
        db.session.add(user)