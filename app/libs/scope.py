# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/6/9 15:47
# @Author  : lemon


class BaseScope:
    allow_api    = []
    allow_module = []
    forbidden    = []

    def __add__(self,other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))

        return self



class UserScope(BaseScope):
    forbidden = ['v1.user+super_get_user',
                 'v1.user+super_delete_user',]

    def __init__(self):
        pass



class AdminScope(BaseScope):

    allow_module = ['v1.user']

    def __init__(self):
        pass



def is_in_scope(scope,endpoint):
    scope = globals()[scope]()
    temp = endpoint.split('+')
    allow_module = temp[0]

    if endpoint in scope.forbidden:
        return False
    elif  endpoint in scope.allow_api:
        return True
    elif allow_module in scope.allow_module:
        return True
    else:
        return False

