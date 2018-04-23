import json

import fakeredis

from chatbot import session


def test_get_none_existent_employee(mocker):
    redis_mock = mocker.patch('redis.from_url')
    redis_mock.return_value = fakeredis.FakeStrictRedis()

    assert None is session.get_employee(42)


def test_get_existent_employee(mocker):
    fake_redis_client = fakeredis.FakeStrictRedis()
    fake_redis_client.set('chatbot:employee:42', '{"foo":"bar"}')
    redis_mock = mocker.patch('redis.from_url')
    redis_mock.return_value = fake_redis_client

    assert {"foo": "bar"} == session.get_employee(42)


def test_employee_id(mocker):
    fake_redis_client = fakeredis.FakeStrictRedis()
    fake_redis_client.set('chatbot:employee:42', '{"foo":"bar"}')
    redis_mock = mocker.patch('redis.from_url')
    redis_mock.return_value = fake_redis_client

    assert session.employee_exists(42)
    assert not session.employee_exists(1337)


def test_set_new_employee(mocker):
    redis_mock = mocker.patch('redis.from_url')
    fake_redis_client = fakeredis.FakeStrictRedis()
    redis_mock.return_value = fake_redis_client

    session.set_employee(1337, {'foo': 'bar'})
    assert {'foo': 'bar'} == json.loads(fake_redis_client.get('chatbot:employee:1337'))
