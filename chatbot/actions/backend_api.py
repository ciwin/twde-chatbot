from chatbot.config import Config
import requests
import logging

conf = Config()
logger = logging.getLogger(__name__)


def validate_response(response):
    if response.status_code >= 300:
        return None
    else:
        return response.json()


def _login_name(email):
    return email.split('@')[0]


def get_employee(email):
    url = conf.get_value('backend-api-base-url') + 'people/' + _login_name(email)
    return validate_response(requests.get(url, headers={'Authorization': conf.get_value('backend-api-token')}))


def get_leave(employee_id):
    url = conf.get_value('backend-api-base-url') + 'leave?employee_ids=' + employee_id
    return validate_response(requests.get(url, headers={'Authorization': conf.get_value('backend-api-token')}))
