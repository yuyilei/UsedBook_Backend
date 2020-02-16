
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
    page = request.args.get("page", 1, type=int)
    per_page = 15
    book_id = request.args.get("book_id")
    book = Book.query.filter_by(id=book_id).first()
    comments = list(book.comments)
    start = (page-1)*per_page
    end = min(page*per_page, len(comments))
    comments = comments[start:end]
    if book is None:
        return jsonify({
            "message": "book does not exist!"
        }), 404
    return jsonify({
        "message": "success",
        "book": book.detail_json(g.current_user),
        "comments": [comment.display_json() for comment in comments],
        "comment_count": len(comments),
    }), 200

