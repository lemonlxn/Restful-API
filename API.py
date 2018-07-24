# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/27 20:26
# @Author  : lemon

from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.base_exception import BaseException
from app.libs.exception import ServerException

app = create_app()

@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e,BaseException):
        return e
    elif isinstance(e,HTTPException):
        code = e.code
        msg  = e.description
        error_code = 1007
        return BaseException(msg,code,error_code)
    else:
        if not app.config['DEBUG']:
            return ServerException()
        else:
            return e



if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'],host='0.0.0.0',port=5100)