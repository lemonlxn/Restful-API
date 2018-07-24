# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/28 21:39
# @Author  : lemon
from flask import jsonify
from sqlalchemy import or_

from app.libs.redprint import Redprint
from app.models.book import Book
from app.validators.forms import BookSearchForm

api = Redprint('book')

@api.route('/search')
def search():
    form = BookSearchForm().validate_parameter_for_api()
    q = '%' + form.q.data +'%'

    books = Book.query.filter(
        or_(Book.title.like(q),Book.publisher.like(q))).all()

    books = [book.hide('summary','price') for book in books]

    return jsonify(books)


@api.route('/<isbn>/detail')
def detail(isbn):
    book = Book.query.filter_by(isbn=isbn).first_or_404()
    return jsonify(book)