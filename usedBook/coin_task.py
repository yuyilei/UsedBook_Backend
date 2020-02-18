import redis
import time
import datetime
import uuid

from . import app, db
from .models import User

rds = redis.Redis(host=app.config['REDIS_HOSTNAME'], port=app.config['REDIS_PORT'])

task_limit_times = {"login":1, "collect": 5, "publish": 5, "comment":5}
inital_task = {"login":0, "collect":0, "publish": 0, "comment": 0}
task_coin = {"login": 5, "collect": 2, "publish": 2, "comment": 2}

def tomorrow():
    return int(time.mktime(datetime.date.today().timetuple())) + 86400

def update_daily_task(user, task):
    """
    先更新task次数
    再更新user的coin
    """
    if update_daily_task_count(user.id, task):
        update_user_coin(user, task)
        return True
    return False

def update_user_coin(user, task):
    """
    更新coin个数
    """
    coin = task_coin.get(task)
    if coin is None:
        return False
    user.coins += coin
    db.session.add(user)
    db.session.commit()

def update_daily_task_count(user_id, task):
    """
    跟新用户每日任务的执行次数
    """

    hashname = "userid-%s" % user_id
    expire_time = tomorrow()
    # 当天还没开始执行任何任务
    if rds.exists(hashname) == 0:
        # 创建任务，设置超时时间
        rds.hmset(hashname, inital_task)
        rds.hset(hashname, task, 1)
        rds.expire(hashname, expire_time)
        return True

    task_limit = task_limit_times.get(task)
    if task_limit is None:
        return False
    task_count = int(rds.hget(hashname, task))
    # 当前执行此任务还未达到上限
    if task_count < task_limit:
        new_count = task_count + 1
        rds.hset(hashname, task, new_count)
        return True
    # 执行达到上限
    return False


def get_daily_task(user_id):
    """
    获取用户每日任务的执行次数
    """
    hashname = "userid-%s" % user_id
    if rds.exists(hashname) == 0:
        return inital_task
    tasks = rds.hgetall(hashname)
    if tasks is None:
        return inital_task
    return {str(k, encoding="utf8"): int(v) for k, v in tasks.items()}


