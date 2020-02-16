"""
    POST /book/comment/ 发送评论
"""

from flask import jsonify, request, g
from . import book
from ..models import Book, Comment
from ..decorators import login_required
from .. import db


@book.route("/comment/", methods=["POST"])
@login_required
def post_comment():
    content = request.get_json().get("content")
    book_id = request.get_json().get("book_id")
    reply_id = request.get_json().get("reply_id")
    commentator_id = g.current_user.id
    comment = Comment(
                content = content,
                book_id = book_id,
                commentator_id = commentator_id,
            )

    if reply_id != None:
        comment.reply_id = reply_id
    db.session.add(comment)
    db.session.commit()
    return jsonify({
            "message": "success",
        }), 200

