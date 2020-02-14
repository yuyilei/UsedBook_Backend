"""
    GET  /user/bought/  获取改用户买到的全部的图书
"""

from flask import jsonify, request, g
from . import user
from ..models import Book, User
from ..decorators import login_required
from .. import db

@user.route('/bought/', methods=['GET'])
@login_required
def bought():
    user = g.current_user
    page = request.args.get('page', 1, type=int)
    per_page = 10
    records = user.records
    book_list = []
    for record in records:
        book = Book.query.filter_by(id=record.book_id).first()
        if book != None:
            book_list.append(book)

    start = (page-1)*per_page
    end = max(page*per_page, len(book_list))
    book_list = book_list[start:end]
    return jsonify({
            "message": "success",
            "book_list" : [book.publish_json(user) for book in book_list],
            "book_num": len(book_list),
        }), 200
