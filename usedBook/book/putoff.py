"""
    PUT /book/putoff  图书下架
"""

from flask import jsonify, request, g
from . import book
from ..models import Book
from ..decorators import login_required
from .. import db

@book.route('/putoff/', methods=['PUT'])
@login_required
def putoff():
    """
    图书发布者将图书下架
    """
    book_id = request.get_json().get('book_id')
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({
                "message" : "book doest not exist!",
            }), 404
    if book.publisher is not g.current_user:
        return jsonify({
                "message" : "no permission to put off the book",
            }), 403
    if book.is_selt is True:
        return jsonify({
                "message" : "the book is already selt!",
            }), 403
    if book.on_sell is False:
        return jsonify({
                "message" : "the book is already not on sell",
            }), 403

    book.on_sell = False
    db.session.add(book)
    db.session.commit()
    return jsonify({
            "message" : "put off the book successfully!",
        }), 200
