"""
   POST  /auth/username/   登录
"""

from . import auth
from flask import request, jsonify, g
from ..models import User
from .. import db, app
from ..decorators import login_required


@auth.route("/username/", methods=["POST"])
@login_required
def username():
    username = request.get_json().get("username")
    user = g.current_user
    user.username = username
    db.session.add(user)
    db.session.commit()
    return jsonify({
            "message": "success"
        }), 200

