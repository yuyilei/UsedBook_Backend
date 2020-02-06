"""
    POST /book/purchase/  购买图书
"""

from flask import jsonify, request, g
from . import book
from ..models import Book, Record
from ..decorators import login_required
from .. import db, app


@book.route('/purchase/', methods=['POST'])
@login_required
def purchase():
    """
    购买图书
    分布式锁redis
    """
    book_id = request.get_json().get("book_id")
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({
                "message" : "book does not exist"
            }), 404
    if book.is_selt is True:
        return jsonify({
                "message" : "the book have been bought"
            }), 403
    # try to get lock
    # then...
    record = Record(
                buyer_id = g.current_user.id,
                book_id = book_id,
            )
    book.is_selt = True
    db.session.add(book)
    db.session.add(record)
    db.session.commit()
    return jsonify({
            "message" : "buy the book successfully!"
        }), 200
