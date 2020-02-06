"""
    PUT /book/puton  图书上架
"""

from flask import jsonify, request, g
from . import book
from ..models import Book
from ..decorators import login_required
from .. import db

@book.route('/puton/', methods=['PUT'])
@login_required
def puton():
    """
    图书发布者将图书上架
    """
    book_id = request.get_json().get('book_id')
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({
                "message" : "book doest not exist!",
            }), 404
    if book.publisher is not g.current_user:
        return jsonify({
                "message" : "no permission to put on the book",
            }), 403
    if book.is_selt is True:
        return jsonify({
                "message" : "the book is already selt!",
            }), 403
    if book.on_sell is True:
        return jsonify({
                "message" : "the book is already on sell",
            }), 403

    book.on_sell = True
    db.session.add(book)
    db.session.commit()
    return jsonify({
            "message" : "put on the book successfully!",
        }), 200
