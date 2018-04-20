import logging

import requests

from chatbot.actions import middlewares
from chatbot.config import CONF

logger = logging.getLogger(__name__)
BASE_API_URL = CONF.get_value('backend-api-base-url')


def _login_name(email):
    return email.split('@')[0]


@middlewares.valid_response
def get_employee(email):
    url = BASE_API_URL + 'people/' + _login_name(email)
    return requests.get(url, headers={'Authorization': CONF.get_value('backend-api-token')})


@middlewares.valid_response
def get_leaves(employee_id):
    url = BASE_API_URL + 'leave?employee_ids=' + employee_id
    return requests.get(url, headers={'Authorization': CONF.get_value('backend-api-token')})


def post_leave(leave):
    url = BASE_API_URL + 'leave'
    response = requests.post(url, json=leave, headers={'Authorization': CONF.get_value('backend-api-token')})
    return response.status_code == 201
