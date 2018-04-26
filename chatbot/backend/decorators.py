import functools
import logging

from chatbot.backend.errors import BackendError

logger = logging.getLogger(__name__)


def valid_response(func):
    @functools.wraps(func)
    def _valid_response(*args, **kw):
        response = func(*args, **kw)
        if response.status_code >= 300:
            raise BackendError(
                "Got invalid response: " + str(response.status_code))
        else:
            return response.json()

    return _valid_response
