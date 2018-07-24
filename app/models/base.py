# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/10 12:03
# @Author  : lemon

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy,BaseQuery
from sqlalchemy import Column,Integer,SmallInteger
from contextlib import contextmanager

from app.libs.exception import NotFoundException


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


# 改写filter_by

class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if not 'status' in kwargs.keys():
            # 默认status = 1 ，用filter_by查询数据，只有status = 1的数据才会被查询出来
            kwargs['status'] = 1
        return super(Query,self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if rv is None:
            raise NotFoundException()
        return rv

    def first_or_404(self):
        rv = self.first()
        if rv is None:
            raise NotFoundException()
        return rv

# 传入自定义Query类
db = SQLAlchemy(query_class=Query)

class Base(db.Model):
    __abstract__ = True    # 代表这是一个基类，不会给Base创建表
    create_time = Column('create_time',Integer) # 类变量一旦设置默认值，则实例该变量的时候，所有值相同
    status = Column(SmallInteger,default=1)     # status = 0 代表软删除

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def __getitem__(self, item):
        return getattr(self,item)

    def set_attrs(self,form_data):
        '''
        检测模型里面，与提交的表单是否有相同字段，如果有的话，进行动态赋值。
        '''
        for key,value in form_data.items():
            if hasattr(self,key) and key != 'id':
                setattr(self,key,value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0


    def keys(self):
        return self.fields

    def hide(self,*keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self,*keys):
        for key in keys:
            self.fields.append(key)
        return self