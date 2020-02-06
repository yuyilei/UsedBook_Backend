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
    comments = db.relationship('Comment', backref='commentator', lazy='dynamic', cascade='all')
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
        return s.dumps({'id': self.id})


    @staticmethod
    def verify_auth_token(token):
        """
        verify user from user
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.load(token)
        except:
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
    is_selt = db.Column(db.Boolean, default=False)
    on_sell = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(164))
    title = db.Column(db.Text)
    information = db.Column(db.Text)
    contact = db.Column(db.Text)
    pushlish_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    edit_time = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='book', lazy='dynamic', cascade='all')

class Record(db.Model):
    """
    购买记录
    """
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    record_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pushlisher_id = db.Column(db.Integer, db.ForeignKey('users.id'))


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

