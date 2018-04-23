import json

import redis

from chatbot.config import CONF

_CLIENT = None


def _get_client():
    global _CLIENT
    if not _CLIENT:
        _CLIENT = redis.from_url(CONF.get_value('redis-url'))
    return _CLIENT


def _get_key(id):
    return "chatbot:employee:{}".format(id)


def get_employee(id):
    val = _get_client().get(_get_key(id))
    return json.loads(val)


def set_employee(id, info):
    info = json.dumps(info)
    _get_client().set(_get_key(id), info, ex=CONF.get_value('redis-expire-time'))


def have_employee_id(id):
    return _get_client().exists(_get_key(id))
