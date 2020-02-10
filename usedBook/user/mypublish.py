"""
    GET  /user/mypublish/  获取改用户发布的全部的图书
"""

from flask import jsonify, request, g
from . import user
from ..models import Book, User
from ..decorators import login_required
from .. import db


@user.route('/mypublish/', methods=['GET'])
@login_required
def mypublish():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({
                "message": "user does not exist",
            }), 404

    print(len(list(user.books)))
    book_list = list(user.books)
    return jsonify({
            "message": "success",
            "book_list" : [book.publish_json() for book in book_list],
            "book_num": len(book_list),
        }), 200


