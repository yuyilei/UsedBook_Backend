import os
basedir = os.path.abspath(os.path.dirname(__file__))

"""
common configuration
 -- SECRET_KEY: secret key
 -- SQLALCHEMY_COMMIT_ON_TEARDOWN: True

 -- SQLALCHEMY_RECORD_QUERIES:
    -- Can be used to explicitly disable or enable query recording.
       Query recording automatically happens in debug or testing mode.

 -- SQLALCHEMY_TRACK_MODIFICATIONS:
    -- If set to True, Flask-SQLAlchemy will track modifications of
       objects and emit signals.
       The default is None, which enables tracking but issues a warning that
       it will be disabled by default in the future.
       This requires extra memory and should be disabled if not needed.

 more configuration keys please see:
  -- http://flask-sqlalchemy.pocoo.org/2.1/config/#configuration-keys
"""
class Config:
    """common configuration"""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    """mail configuration"""
    REDIS_BROKER_HOSTNAME = os.getenv('REDIS_BROKER_HOSTNAME')
    REDIS_BACKEND_HOSTNAME = os.getenv('REDIS_BACKEND_HOSTNAME')

    """celery configuration"""
    CELERY_BROKER_URL = 'redis://{}:6385/1'.format(os.environ.get('REDIS_BROKER_HOSTNAME'))
    CELERY_RESULT_BACKEND = 'redis://{}:6386/1'.format(os.environ.get('REDIS_BACKEND_HOSTNAME'))

    # SQLALCHEMY_DATABASE_URI = os.environ.get("USEDBOOK_DATABASE_SQL") or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data-test.sqlite")

    WX_APPID = os.getenv('WX_APPID')
    WX_APPSECRET = os.getenv('WX_APPSECRET')

    @staticmethod
    def init_app(app):
        pass

"""
development configuration
 -- DEBUG: debug mode
 -- SQLALCHEMY_DATABASE_URI:
    -- The database URI that should be used for the connection.

more connection URI format:
 -- Postgres:
    -- postgresql://scott:tiger@localhost/mydatabase
 -- MySQL:
    -- mysql://scott:tiger@localhost/mydatabase
 -- Oracle:
    -- oracle://scott:tiger@127.0.0.1:1521/sidname
"""
class DevelopmentConfig(Config):
    """development configuration"""
    DEBUG = True

"""
testing configuration
 -- TESTING: True
 -- WTF_CSRF_ENABLED:
    -- in testing environment, we don't need CSRF enabled
"""
class TestingConfig(Config):
    """testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data-test.sqlite")
    WTF_CSRF_ENABLED = False

# production configuration
class ProductionConfig(Config):
    """production configuration"""
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI" )

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    "develop": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}

