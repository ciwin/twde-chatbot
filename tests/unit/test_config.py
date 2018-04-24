import os
from contextlib import contextmanager

from chatbot.config import CONF


@contextmanager
def _setup_environ(name, new_value):
    original_value = os.getenv(name)
    try:
        os.environ[name] = new_value
        yield
    finally:
        if original_value:
            os.environ[name] = original_value
        else:
            del os.environ[name]


def test_load_config_from_file():
    with _setup_environ('HANGOUTS_API_KEY', ''):
        assert "secret-api-key" == CONF.get_value("hangouts-api-key")


def test_load_config_from_environment_value():
    with _setup_environ('HANGOUTS_API_KEY', 'foobar'):
        assert "foobar" == CONF.get_value("hangouts-api-key")
