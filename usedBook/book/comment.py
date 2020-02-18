"""
    POST /book/comment/ 发送评论
    GET /book/comment/ 获取评论
    DELETE /book/comment/ 删除评论
"""

from flask import jsonify, request, g
from . import book
from ..models import Book, Comment
from ..decorators import login_required
from .. import db
from ..coin_task import update_daily_task


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
                reply_id = reply_id,
            )

    if reply_id != None:
        comment.reply_id = reply_id
    db.session.add(comment)
    db.session.commit()
    coin_task_success = update_daily_task(g.current_user, "comment")
    return jsonify({
            "message": "success",
            "coin_task_success": coin_task_success,
        }), 200


@book.route("/comment/", methods=["GET"])
@login_required
def get_comment():
    book_id = request.args.get("book_id")
    page = request.args.get("page", 1, type=int)
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({
                "message": "book does not exist",
            }), 404

    comments = list(book.comments)
    per_page = 10
    start = (page-1)* per_page
    end = min(page*per_page, len(comments))
    comments = comments[start:end]
    return jsonify({
        "message": "success",
        "comments": [comment.to_json() for comment in comments],
        "comment_count": len(comments),
        }), 200



@book.route("/comment/", methods=["DELETE"])
@login_required
def delete_comment():
    comment_id = request.get_json().get("comment_id")
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is None:
        return jsonify({
                "message": "comment does not exist",
            }), 404
    if comment.commentator_id != g.current_user.id:
        return jsonify({
                "message": "no permssion to delete"
            }), 403
    db.session.delete(comment)
    db.session.commit()
    return jsonify({
            "message": "success",
        }), 200

