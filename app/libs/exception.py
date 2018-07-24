# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/6/1 15:36
# @Author  : lemon


from app.libs.base_exception import BaseException


class ClientTypeException(BaseException):
    code = 400
    msg = 'client is invalid'
    error_code = 1006

class ParameterException(BaseException):
    code = 400
    msg  = 'invalid parameter'
    error_code = 1000


class Success(BaseException):
    code = 201
    msg  = 'Success'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = -1


class ServerException(BaseException):
    code = 500
    msg = 'sorry,we make a mistake'
    error_code = 999

class NotFoundException(BaseException):
    code = 404
    msg = 'the resource are not_found 0__0...'
    error_code = 1001

class AuthFailedException(BaseException):
    code = 401
    msg = 'authorization failed'
    error_code = 1005

class ForbiddenException(BaseException):
    code = 403
    msg = 'Forbidden, not in scope'
    error_code = 1004

class DuplicateGift(BaseException):
    code = 400
    error_code = 2001
    msg = 'the current book has already in gift'