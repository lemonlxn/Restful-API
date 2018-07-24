# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/6/1 15:54
# @Author  : lemon
from flask import request,json
from werkzeug.exceptions import HTTPException


class BaseException(HTTPException):
    '''
    自定义错误异常信息
    '''
    msg = 'sorry,we make a mistake'
    code = 500
    error_code = 999

    def __init__(self,msg=None,code=None,error_code=None,
                 headers=None):
        if msg:
            self.msg = msg
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code

        super(BaseException,self).__init__(msg,None)

    def get_body(self, environ=None):
        body = dict(
            msg = self.msg,
            error_code = self.error_code,
            request = request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text


    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        '''
        获取问号之前的url路径
        '''
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]



