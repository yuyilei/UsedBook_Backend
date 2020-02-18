"""
    PUT /book/collect 收藏图书
    PUT /book/uncollect 取消收藏图书
"""

from flask import jsonify, request, g
from . import book
from ..models import Book
from ..decorators import login_required
from .. import db
from ..coin_task import update_daily_task


@book.route('/collect/', methods=['PUT'])
@login_required
def collect():
    """
    收藏图书
    """
    book_id = request.get_json().get('book_id')
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({
                "message" : "book does not exist!",
            }), 404
    if book in g.current_user.collections:
        return jsonify({
                "message" : "already collect the book"
            }), 403
    user = g.current_user
    user.collections.append(book)
    db.session.add(user)
    db.session.commit()
    coin_task_success = update_daily_task(g.current_user, "collect")
    return jsonify({
            "message" : "collect the book successfully",
            "coin_task_success": coin_task_success,
        }), 200


@book.route('/uncollect/', methods=['PUT'])
@login_required
def uncollect():
    """
    取消收藏图书
    """
    book_id = request.get_json().get('book_id')
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({
                "message" : "book does not exist!",
            }), 404
    if book not in g.current_user.collections:
        return jsonify({
                "message" : "have not collected the book"
            }), 403
    user = g.current_user
    user.collections.remove(book)
    db.session.add(user)
    db.session.commit()
    return jsonify({
            "message" : "collect the book successfully",
        }), 200



