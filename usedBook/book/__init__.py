from flask import Blueprint

book = Blueprint(
        'book',
        __name__,
)

from . import publish, puton, putoff, collect, purchase, market, detail, delete, comment, search
