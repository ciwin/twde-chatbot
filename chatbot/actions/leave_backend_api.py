from chatbot.config import CONF
import jwt
import requests
from chatbot.actions.errors import BackendError

def get_leave_entitlement(employee, year):
    homeOffice = employee.get('homeOffice').get('name')
    request_body = {'employeeId': employee.get('employeeId'), 'year': year, 'homeOffice': homeOffice}
    jwt_token = jwt.encode(request_body, CONF.get_value('timeoff-api-key'), algorithm='HS256')
    response = requests.get(CONF.get_value('timeoff-api-url'), headers={'Authorization': 'Bearer %s' % jwt_token.decode("utf-8")})
    
    if response.status_code != 200:
        raise BackendError("Got invalid response: " + str(response.status_code))
    
    return response.json()