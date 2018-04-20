import pytest

from chatbot.actions import backend_api
from chatbot.actions.errors import BackendError


class FakeResponse(object):
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


def test_get_employee(mocker):
    mock_request = mocker.patch('requests.get')
    mock_request.return_value = FakeResponse(200, {'name': 'foobar'})
    assert {'name': 'foobar'} == backend_api.get_employee('foo@bar')
    mock_request.assert_called_with('http://google.de/people/foo', headers={'Authorization': 'secret-token'})


def test_invalid_response_get_employee(mocker):
    mock_request = mocker.patch('requests.get')
    mock_request.return_value = FakeResponse(404, None)
    with pytest.raises(BackendError):
        backend_api.get_employee('foo@bar')
    mock_request.assert_called_with('http://google.de/people/foo', headers={'Authorization': 'secret-token'})


def test_get_leaves(mocker):
    mock_request = mocker.patch('requests.get')
    mock_request.return_value = FakeResponse(200, [{'name': 'leave1'}])
    assert [{'name': 'leave1'}] == backend_api.get_leaves('1337')
    mock_request.assert_called_with('http://google.de/leave?employee_ids=1337',
                                    headers={'Authorization': 'secret-token'})


def test_post_leave(mocker):
    mock_request = mocker.patch('requests.post')
    mock_request.return_value = FakeResponse(201, None)
    assert True is backend_api.post_leave({'leaveId': 42})
    mock_request.assert_called_with('http://google.de/leave', headers={'Authorization': 'secret-token'},
                                    json={'leaveId': 42})


def test_post_leave_invalid(mocker):
    mock_request = mocker.patch('requests.post')
    mock_request.return_value = FakeResponse(400, None)
    assert False is backend_api.post_leave({'leaveId': 42})
    mock_request.assert_called_with('http://google.de/leave', headers={'Authorization': 'secret-token'},
                                    json={'leaveId': 42})

    mock_request = mocker.patch('requests.post')
    mock_request.return_value = FakeResponse(503, None)
    assert False is backend_api.post_leave({'leaveId': 42})
    mock_request.assert_called_with('http://google.de/leave', headers={'Authorization': 'secret-token'},
                                    json={'leaveId': 42})
