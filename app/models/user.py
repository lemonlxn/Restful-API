# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/31 21:07
# @Author  : lemon


from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash,check_password_hash

from app.libs.exception import  AuthFailedException
from app.models.base import Base


class User(Base):
    id = Column(Integer,primary_key=True)
    email = Column(String(24),unique=True,nullable=False)
    nickname = Column(String(24),unique=True)
    auth = Column(SmallInteger,default=1)
    _password=Column('password',String(100))

    def keys(self):
        return ['id','email','nickname','auth']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def verify(email,password):
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailedException()
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid':user.id,'scope':scope}               # 如果以上验证都通过，返回用户信息



    def check_password(self,raw):
        if not self._password:
            return False
        return check_password_hash(self._password,raw)



