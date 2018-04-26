import jwt
import requests

from chatbot.backend import decorators
from chatbot.config import CONF


@decorators.valid_response
def get_leave_entitlement(employee, year):
    request_body = {
        'employeeId': employee.get('employeeId'),
        'year': year,
        'homeOffice': employee.get('homeOffice').get('name')
    }
    jwt_token = jwt.encode(request_body, CONF.get_value('leave-api-key'), algorithm='HS256')

    return requests.get(CONF.get_value('leave-api-url') + 'leave-entitlement',
                        headers={'Authorization': 'Bearer %s' % jwt_token.decode("utf-8")})
