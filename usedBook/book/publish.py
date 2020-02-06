
"""
    POST /book/publish/  发布书
"""

from flask import jsonify, request, g
from . import book
from ..models import Book, Tag
from ..decorators import login_required
from .. import db


@book.route('/publish/', methods=['POST'])
@login_required
def publish():
    """
    用户发布二手书
    todo:
        Tag
    """
    picture = request.get_json().get('picture')
    price = request.get_json().get('price')
    name = request.get_json().get('name')
    title = request.get_json().get('title')
    contact = request.get_json().get('contact')
    information = request.get_json().get('information')
    tags = request.get_json().get('tags')

    try:
        book = Book(
            price = int(price),
            name = name,
            title = title,
            picture = picture,
            information = information,
            contact = contact,
            publisher_id = g.current_user.id,
        )
        db.session.add(book)
        db.session.commit()
    except Exception as e:
        return jsonify({'message': 'add book to database failed, ex= %s' % repr(e)}), 500

    else:
        # create tags
        message = "add book and create tags succeed"
        try:
            tags_list = list(set(tags))
            for tag in tags_list:
                _tag = Tag.query.filter_by(content=tag).first()
                if _tag is None:
                    # if the tag does not exist, create it first
                    _tag = Tag(
                            content = tag,
                    )
                _tag.books.append(book)
            db.session.commit()
        except Exception as e:
            message = "add book succeed, however create tag failed, ex= %s" % repr(e)
        finally:
            return jsonify({
                    "message" : message,
                    "book_id" : book.id,
                }), 200
