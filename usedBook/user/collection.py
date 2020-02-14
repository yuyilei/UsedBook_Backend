"""
    GET  /user/collection/  获取改用户收藏的全部的图书
"""

from flask import jsonify, request, g
from . import user
from ..models import Book, User
from ..decorators import login_required
from .. import db

@user.route('/collection/', methods=['GET'])
@login_required
def collection():
    user = g.current_user
    page = request.args.get('page', 1, type=int)
    per_page = 10
    book_list = list(user.collections)
    start = (page-1)*per_page
    end = max(page*per_page, len(book_list))
    book_list = book_list[start:end]
    return jsonify({
            "message": "success",
            "book_list" : [book.publish_json(user) for book in book_list],
            "book_num": len(book_list),
        }), 200
