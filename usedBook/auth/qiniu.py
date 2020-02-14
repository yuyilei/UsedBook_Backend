"""
    GET /auth/qiniu/ 获取七牛的token和budget
"""

from flask import jsonify, request, g
from . import auth
from ..decorators import login_required
from .. import app
from qiniu import Auth, put_file, etag
import qiniu.config
import time

access_key = app.config['QINIU_ACCESS_KEY']
secret_key = app.config['QINIU_SECRET_KEY']
bucket_name = app.config['QINIU_BUCKET_NAME']

def generate_token():
    q = Auth(access_key, secret_key)
    bucketname = "usedbook-storage"
    filename = None
    token = q.upload_token(bucketname, filename, 3600)
    return token

@auth.route('/qiniu/', methods=['GET'])
@login_required
def qiuniu():
    """
    获取七牛的
    """
    return jsonify({
            "token": generate_token(),
            "bucketname": bucket_name,
            "message": "success",
        }), 200




