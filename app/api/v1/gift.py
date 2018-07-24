# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/6/23 15:23
# @Author  : lemon
from flask import g

from app import db
from app.libs.exception import DuplicateGift, Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.book import Book
from app.models.gift import Gift

api = Redprint('gift')

@api.route('/<isbn>',methods = ['POST'])
@auth.login_required
def create(isbn):
    uid = g.user.uid
    with db.auto_commit():
        Book.query.filter_by(isbn=isbn).first_or_404()  # 首先判断该本书，是否在数据库中
        gift = Gift.query.filter_by(isbn=isbn,uid=uid).first()  # 检测礼物的重复性
        if gift:
            raise DuplicateGift()
        gift = Gift()
        gift.isbn = isbn
        gift.uid  = uid
        db.session.add(gift)
    return Success()



