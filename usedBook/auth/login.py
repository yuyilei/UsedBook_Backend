"""
   POST  /auth/login/   登录
"""

import requests
from . import auth
from flask import request, jsonify
from ..models import User
from .. import db, app

wx_appid = app.config['WX_APPID']
wx_appsecret = app.config['WX_APPSECRET']
wx_openid_url = "https://api.weixin.qq.com/sns/jscode2session"

@auth.route('/login/', methods=['POST'])
def login():
    """
    request:
        code: string
    response:
        token: string
        message: string
        success: bool
    """
    code = request.get_json().get("code")
    if code is None:
        return jsonify({
            'success': False,
            'message': 'code can not be none!',
            }), 400

    payload = {'appid': wx_appid, 'secret': wx_appsecret, 'js_code': code, 'grant_type': 'authorization_code'}
    r = requests.get(wx_openid_url, params=payload)
    if r.status_code != 200:
        return jsonify({
            'success': False,
            'message': 'request status code is %s' %  r.status_code,
            }), 401

    try:
        rj = r.json()
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'response jsonify failed, ex= %s' % e.message,
            }), 401
    else:
        if rj.get('openid') is not None:
            user_id = None
            # check in User
            openid = rj['openid']
            u = User.query.filter_by(open_id=openid).first()
            token = ""
            message = ""
            if u is not  None:
                token = u.generate_auth_token()
                user_id = u.id
                message = "not first login"
            else:
                # generate that user
                try:
                    user = User(open_id=openid)
                    db.session.add(user)
                    db.session.commit()
                    token = user.generate_auth_token()
                    user_id = user.id
                except Exception as e:
                    message = "failed in generating the user, ex= %s" % e.message
                else:
                    message = "first login, and generate that user"
            return jsonify({
                'success': True,
                'token': token,
                'message': message,
                'id': user_id,
                }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'get openid failed, error message=  %s' % rj.get('errmsg'),
                }), 401

