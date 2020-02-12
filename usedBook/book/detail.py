
"""
    GET /book/detail/  获取图书的详细信息
"""

from flask import jsonify, request, g
from . import book
from ..models import Book, User
from ..decorators import login_required
from .. import db


@book.route('/detail/', methods=['GET'])
@login_required
def detail():
    book_id = request.args.get('book_id')
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({
            "message": "book does not exist!"
        }), 404
    return jsonify({
        "message": "success",
        "book": book.detail_json(g.current_user),
    }), 200

