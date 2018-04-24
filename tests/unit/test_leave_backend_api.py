import pytest
from chatbot.actions import leave_backend_api
from chatbot.actions.errors import BackendError

class FakeResponse(object):
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data

def test_get_leave_entitlement_should_get_leave_entitlement(mocker):
    employee = {
			"employeeId": "17017",
			"homeOffice": {
				"name": "Hamburg"
			}
		}

    mock_request = mocker.patch('requests.get')
    response_body = {
    	"employeeId": "17017",
    	"homeOffice": "Hamburg",
    	"year": 2018,
    	"leaveEntitlement": 48,
    	"remainingLeave": 43
		}

    mock_request.return_value = FakeResponse(200, response_body)
    assert response_body == leave_backend_api.get_leave_entitlement(employee, 2018)
    
    mock_request.assert_called_with('https://localhost:5000/api/leaveentitlement', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbXBsb3llZUlkIjoiMTcwMTciLCJ5ZWFyIjoyMDE4LCJob21lT2ZmaWNlIjoiSGFtYnVyZyJ9.eguebbyCzJ4wF9PfevQLzxLt4mT6w8pGtmNzkxC-Ics'})

def test_get_leave_entitlement_should_raise_error(mocker):
    employee = {
			"employeeId": "17017",
			"homeOffice": {
				"name": "Hamburg"
			}
		}

    mock_request = mocker.patch('requests.get')
    response_body = {
    	"message": "Invalid token."
		}

    mock_request.return_value = FakeResponse(403, response_body)
		
    with pytest.raises(BackendError):
    	leave_backend_api.get_leave_entitlement(employee, 2018)
    
    mock_request.assert_called_with('https://localhost:5000/api/leaveentitlement', headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbXBsb3llZUlkIjoiMTcwMTciLCJ5ZWFyIjoyMDE4LCJob21lT2ZmaWNlIjoiSGFtYnVyZyJ9.eguebbyCzJ4wF9PfevQLzxLt4mT6w8pGtmNzkxC-Ics'})
