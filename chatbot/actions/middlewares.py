import functools
import logging

logger = logging.getLogger(__name__)


def valid_response(func):
    @functools.wraps(func)
    def _valid_response(*args, **kw):
        response = func(*args, **kw)
        if response.status_code >= 300:
            logger.debug("Got invalid response: %s", response)
            return None
        else:
            return response.json()

    return _valid_response
