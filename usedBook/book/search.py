"""
   GET /book/seacrch/  搜索图书
"""

import redis
from flask import jsonify, request, g
from . import book
from ..models import Book, Tag
from ..decorators import login_required
from .. import db, app
from .kmp import kmp

rds = redis.Redis(host=app.config['REDIS_HOSTNAME'], port=app.config['REDIS_PORT'])

def search_with_cache(keyword):
    """
        redis lru cache

    """
    # 获取所用lru的
    # rds.ltrim("lruList" , 1, 0)
    lrukeys = rds.lrange("lruList", 0, -1)
    sorts = {}
    cache_title_result = []
    cache_tag_result = []
    title_result = []    # 来自cache
    tag_result = []
    prekey_result = []
    results = []

    for book in lrukeys:
        _book = eval(book)
        title = _book.get('title')
        tags = _book.get('tags')
        pre_key = _book.get('pre_key')


        if is_on_sell(_book['id']):
            if keyword in str(title):
                sorts[book] = kmp(title, keyword)
            elif keyword in str(tags):
                    cache_tag_result.append(book)
            elif keyword in str(pre_key):
                    prekey_result.append(book)

    # 对title search的结果进行排序
    if len(sorts) != 0:
        sort_list = sorted(sorts.iteritems(), key=lambda d: d[1])
        cache_title_result = [each[0] for each in sort_list]

    # 找出相关tag
    tag = Tag.query.filter_by(content=keyword).first()
    if tag != None:
        books = tag.books.all()
        for book in books:
            if book.on_sell:
                tag_result.append(book.market_json(g.current_user))

    # 找出以keyword开头的book
    books = Book.query.filter(Book.name.startswith(keyword)).all()
    if books != None:
        for book in books:
            if book.on_sell:
                title_result.append(book.market_json(g.current_user))

    insert_lruList(keyword, prekey_result, results, update=False)
    insert_lruList(keyword, title_result, results, update=False)
    insert_lruList(keyword, tag_result, results, update=False)
    insert_lruList(keyword, cache_title_result, results, update=True)
    insert_lruList(keyword, cache_tag_result, results, update=True)
    pop_lruList()
    return results

def is_on_sell(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book != None and book.on_sell is True:
        return True
    return False

def update_prekey(keyword, data):
    if data.get("pre_key") is None or keyword not in data.get("pre_key"):
        data['pre_key'] = list(keyword)
    else:
        data['pre_key'].append(keyword)
    return str(data)


def insert_lruList(keyword, pre_result, results, update=True):
    """
    update=true表示这个条目在lrulist中出现过，需要删除原先的条目
    """
    for item in pre_result:
        if update == True:
            rds.lrem("lruList", item, 1)
        if item not in results:
            results.append(item)
        item = update_prekey(keyword, item)
        rds.lpush("lruLish", item)


def pop_lruList():
    lru_len = rds.llen("lruList")
    while lru_len > 150:
        lru.rpop("lruList")
        lru_len -= 1


@book.route("/search/", methods=["GET"])
@login_required
def search():
    keyword = request.args.get("keyword")
    page = request.args.get("page", 1, type=int)
    per_page = 10
    res = search_with_cache(keyword)
    start = (page-1)*per_page
    end = min(page*per_page, len(res))
    book_list = res[start:end]
    return jsonify({
            "message": "success",
            "book_list": book_list,
            "book_count": len(book_list),
        }), 200


