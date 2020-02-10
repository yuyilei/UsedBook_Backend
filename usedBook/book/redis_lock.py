import redis
import time
import uuid

from .. import app

redis_client = redis.Redis(host=app.config['REDIS_HOSTNAME'], port=app.config['REDIS_PORT'])

def acquire_lock(key, acquire_time=4, time_out=10):
    now = time.time()
    end = now + acquire_time
    timestamp = now + time_out
    lock_key = "lock_key:%s" % key
    while time.time() < end:
        if redis_client.setnx(lock_key, timestamp) or \
            (time.time() > float(redis_client.get(lock_key)) and \
             time.time() > float(redis_client.getset(lock_key, timestamp))) :
            return True
        time.sleep(0.01)
    return False

def release_timeout_lock(key):
    lock_key = "lock_key:%s" % key
    if time.time() < float(redis_client.get(lock_key)):
        # 释放过期的锁
        redis_client.delete(lock_key)

def release_lock(key):
    lock_key = "lock_key:%s" % key
    # 释放这个
    redis_client.delete(lock_key)

def redis_decorator(key):
    def _deco(func):
        def call_func(*args, **kwargs):
            acquire_lock(key)
            try:
                func(*args, **kwargs)
            finally:
                release_lock(key)
        return call_func
    return _deco
