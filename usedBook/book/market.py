
"""
    GET /book/market/  获取market首页的图书信息
"""

from flask import jsonify, request, g
from . import book
from ..models import Book, User
from ..decorators import login_required
from .. import db


@book.route('/market/', methods=['GET'])
@login_required
def market():
    user = User.query.filter_by(id=g.current_user.id).first()
    books = Book.query.filter_by(is_selt=False, on_sell=True).all()
    book_list = list(books)
    return jsonify({
            "message": "success",
            "book_list": len(book_list),
            "books": [book.market_json(user) for book in book_list]
        }), 200
