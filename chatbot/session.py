import json

import redis

from chatbot.config import CONF

_CLIENT = None


def _get_client():
    global _CLIENT
    if not _CLIENT:
        _CLIENT = redis.from_url(CONF.get_value('redis-url'))
    return _CLIENT


def _reset_client():
    global _CLIENT
    _CLIENT = None


def _get_key(id):
    return "chatbot:employee:{}".format(id)


def get_employee(id):
    val = _get_client().get(_get_key(id))
    if val:
        return json.loads(val)


# noinspection PyShadowingBuiltins,PyShadowingBuiltins
def set_employee(id, info):
    info = json.dumps(info)
    _get_client().set(_get_key(id), info, ex=CONF.get_value('redis-expire-time'))


def employee_exists(id):
    return _get_client().exists(_get_key(id))
