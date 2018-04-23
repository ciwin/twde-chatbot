import functools
import logging

import jsonschema
from flask import request, json

from chatbot import session
from chatbot.actions import backend_api
from chatbot.actions.errors import BackendError
from chatbot.config import CONF

logger = logging.getLogger(__name__)


def get_error_response(message, status_code=400):
    response = json.jsonify({'error': message})
    response.status_code = status_code
    return response


def is_json(func):
    @functools.wraps(func)
    def _is_json(*args, **kw):
        if not request.get_json():
            return get_error_response('request is not JSON')
        return func(*args, **kw)

    return _is_json


def authenticate(func):
    @functools.wraps(func)
    def _auth(*args, **kw):
        event = request.get_json()
        logger.debug("received %s", event)
        logger.debug("configuratioon token: %s", CONF.get_value("hangouts-api-key"))

        if event.get('token') != CONF.get_value("hangouts-api-key"):
            return get_error_response('Wrong token', 401)
        return func(*args, **kw)

    return _auth


def validate(schema):
    def _inner(func):
        @functools.wraps(func)
        def _validate(*args, **kw):
            body = request.get_json()
            try:
                jsonschema.validate(body, schema)
            except jsonschema.ValidationError as ex:
                response = get_error_response(str(ex))
                return response
            return func(*args, **kw)

        return _validate

    return _inner


def filter_employee_info(employee_info):
    return {k: employee_info[k] for k in ['employeeId', 'homeOffice']}


def fill_session(func):
    @functools.wraps(func)
    def _inner(*args, **kw):
        body = request.get_json()

        if 'message' in body:
            email = body['message']['sender']['email']
            sender_id = body['message']['thread']['name']

            if not session.employee_exists(sender_id):
                try:
                    employee_info = backend_api.get_employee(email)
                except BackendError as ex:
                    logger.warning("fail to fetch employee information from backend: %s", ex)
                else:
                    session.set_employee(sender_id, filter_employee_info(employee_info))

        return func(*args, **kw)

    return _inner
