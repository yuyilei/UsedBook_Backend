"""
    GET  /user/coin/  获取用户的书币信息
"""

from flask import jsonify, request, g
from . import user
from ..models import Book, User
from ..decorators import login_required
from .. import db
from ..coin_task import get_daily_task

@user.route("/coin/", methods=["GET"])
@login_required
def coin():
    tasks = get_daily_task(g.current_user.id)
    coin_count= g.current_user.coins
    return jsonify({
            "message": "success",
            "tasks": tasks,
            "coin_count": coin_count,
        }), 200
