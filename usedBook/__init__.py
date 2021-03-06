
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_moment import Moment
import os
from celery import Celery
from config import config

#定义命名惯例，不需要改
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
#初始化db,将命名惯例naming_convention传给SQL_Alchemy,解决“ValueError: Constraint must have a name"的问题
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'

def create_app(config_name=None,main=True) :
    if config_name is None :
        config_name = 'default'
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("AUTH_SQL") or "sqlite:///" + os.path.join(basedir, 'data.sqlite')

    return app

# from . import auth

app = create_app(config_name = 'default')

@app.route('/')
def hello_world():
    return 'Hello, World!'

from .user import user
app.register_blueprint(user, url_prefix="/user")

from .book import book
app.register_blueprint(book, url_prefix="/book")

from .auth import auth
app.register_blueprint(auth, url_prefix="/auth")
