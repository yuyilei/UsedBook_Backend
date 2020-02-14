"""
    DELETE /book/delete/  删除图书
"""

from flask import jsonify, request, g
from . import book
from ..models import Book, User
from ..decorators import login_required
from .. import db

@book.route('/delete/', methods=['DELETE'])
@login_required
def delete():
    """
    删除图书
    """
    book_id = request.get_json().get("book_id")
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({
                "message": "book does not exist!"
            }), 404
    if book.publisher != g.current_user:
        return jsonify({
                "message": "no permission to delete the book"
            }), 403
    db.session.delete(book)
    db.session.commit()
    return jsonify({
            "message": "success!"
        }), 200

