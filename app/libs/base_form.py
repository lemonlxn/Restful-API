# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/6/3 15:11
# @Author  : lemon
from flask import request
from wtforms import Form

from app.libs.exception import ParameterException


class BaseForm(Form):
    '''
    重写WTForms，将错误信息返回到客户端
    '''
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm,self).__init__(data=data,**args)


    def validate_parameter_for_api(self):
        '''
        返回API参数错误情况
        '''
        valid = super(BaseForm,self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self



