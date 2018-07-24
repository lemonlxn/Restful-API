# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/28 21:35
# @Author  : lemon

from .app import Flask

from app.models.base import db



def create_app():

    app = Flask(__name__)

    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')

    register_blueprint(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app

def register_blueprint(app):

    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(),url_prefix = '/v1')