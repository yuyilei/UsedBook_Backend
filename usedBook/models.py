"""
models.py

    数据库模型
"""

from . import db, login_manager
from itsdangerous import JSONWebSignatureSerializer as Serializer
from itsdangerous import TimedJSONWebSignatureSerializer as TJSSerializer
from random import seed
from flask import current_app, request, url_for
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import AnonymousUserMixin
from sqlalchemy.orm import backref
from datetime import datetime



# a secondary table

UserCollection = db.Table(
        'user_collect',
        db.Column('user_id', db.Integer,
                   db.ForeignKey('users.id', ondelete="CASCADE"),
                   primary_key=True),
        db.Column('book_id', db.Integer,
                   db.ForeignKey('books.id', ondelete="CASCADE"),
                   primary_key=True),
    )

BookTag = db.Table(
        'book_tag',
        db.Column('book_id', db.Integer,
                  db.ForeignKey('books.id', ondelete="CASCADE"),
                  primary_key=True),
        db.Column('tag_id', db.Integer,
                  db.ForeignKey('tags.id', ondelete="CASCADE"),
                  primary_key=True),
    )

class User(db.Model):
    """
    用户表
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(36), index=True)  # weixin openid for identicaion
    username = db.Column(db.String(164))
    biref = db.Column(db.Text)
    college = db.Column(db.String(164))
    coins = db.Column(db.Integer, default = 0)
    sold = db.Column(db.Integer, default = 0)
    books = db.relationship('Book', backref='publisher', lazy='dynamic', cascade='all')
    comments = db.relationship('Comment', backref='commentator', lazy='dynamic', cascade='all')
    records = db.relationship('Record', backref='buyer', lazy='dynamic', cascade='all')
    collections = db.relationship('Book', secondary= UserCollection,
                                  backref=db.backref('collectors', lazy='dynamic'),
                                  lazy='dynamic', cascade='all')


    def generate_auth_token(self):
        """
        generate a token
        """
        s = Serializer(
            current_app.config['SECRET_KEY']
        )
        return str(s.dumps({'id': self.id}), encoding='utf8')


    @staticmethod
    def verify_auth_token(token):
        """
        verify user from user
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as e:
            return None
        else:
            return User.query.get_or_404(data['id'])


class Book(db.Model):
    """
    书表
    """
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    picture = db.Column(db.String(164))
    is_selt = db.Column(db.Boolean, default=False)
    on_sell = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(164))
    title = db.Column(db.Text)
    information = db.Column(db.Text)
    contact = db.Column(db.Text)
    pushlish_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    edit_time = db.Column(db.DateTime, default=datetime.utcnow)
    publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='book', lazy='dynamic', cascade='all')
    tags =  db.relationship("Tag",
                            secondary=BookTag,
                            backref=db.backref('books', lazy='dynamic'),
                            lazy='dynamic', cascade='all')

    def publish_json(self):
        json_book = {
            'id': self.id,
            'price': self.price,
            'picture': self.picture,
            'name': self.name,
            'title': self.title,
            'is_selt': self.is_selt,
            'on_sell': self.on_sell,
            'information': self.information,
            'publish_time': self.pushlish_time,
            'collect_count': len(list(self.collectors)),
        }
        return json_book

    def market_json(self, user):
        islike = True if user in self.collectors else False
        json_book = {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'price': self.price,
            'islike': islike,
            'collect_count': len(list(self.collectors)),
            'image': self.picture,
            'brief': self.information,
        }
        return json_book


    def detail_json(self, user):
        ispublisher = True if self.publisher is user else False
        islike = True if user in self.collectors else False
        tags = "  ".join([tag.content for tag in self.tags])
        json_book = {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'price': self.price,
            'islike': islike,
            'ispublisher': ispublisher,
            'image': self.picture,
            'brief': self.information,
            'collect_count': len(list(self.collectors)),
            'onsell': self.on_sell,
            'finished': self.is_selt,
            'need_connect': self.contact,
            'tags': tags,
        }
        return json_book

class Record(db.Model):
    """
    购买记录
    """
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    record_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))


class Comment(db.Model):
    """
    评论
    """
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    commentator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    content = db.Column(db.Text)


class Tag(db.Model):
    """
    标签
    """
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128), index=True)

