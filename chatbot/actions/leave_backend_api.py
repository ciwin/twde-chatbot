import jwt
import requests

from chatbot.actions import middlewares
from chatbot.config import CONF


@middlewares.valid_response
def get_leave_entitlement(employee, year):
    request_body = {
        'employeeId': employee.get('employeeId'),
        'year': year,
        'homeOffice': employee.get('homeOffice').get('name')
    }
    jwt_token = jwt.encode(request_body, CONF.get_value('leave-api-key'), algorithm='HS256')

    # TODO: change to leave-entitlement when v2 deploys
    return requests.get(CONF.get_value('leave-api-url') + 'leaveentitlement',
                        headers={'Authorization': 'Bearer %s' % jwt_token.decode("utf-8")})
