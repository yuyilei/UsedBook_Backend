"""
    POST /book/purchase/  购买图书
"""

from flask import jsonify, request, g
from . import book
from .redis_lock import acquire_lock, release_lock, release_timeout_lock
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
    if acquire_lock(book_id) is True:
        try:
            record = Record(
                        buyer_id = g.current_user.id,
                        book_id = book_id,
                    )
            book.is_selt = True
            db.session.add(book)
            db.session.add(record)
            db.session.commit()
            # 操作成功，释放锁
            release_lock(book_id)
            return jsonify({
                    "message" : "buy the book successfully!"
                }), 200
        except Exception as e:
            # 释放超时的锁
            release_timeout_lock(book_id)
            return jsonify({
                    "message" : "failed to get lock or database failed, ex= %s" % repr(e)
                }), 500



@book.route('/purchase/', methods=['DELETE'])
@login_required
def delete_purchase():
    """
    删除购买记录
    分布式锁redis
    """
    book_id = request.get_json().get("book_id")
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({
                "message" : "book does not exist"
            }), 404
    if book.is_selt is False:
        return jsonify({
                "message" : "the book have not been bought"
            }), 403
    record = Record.query.filter_by(book_id=book_id).first()
    if record is None:
        return jsonify({
                "message" : "record does not exist"
            }), 404
    # try to get lock
    # then...
    book.is_selt = False
    db.session.add(book)
    db.session.delete(record)
    db.session.commit()
    return jsonify({
            "message" : "delete successfully!"
        }), 200



