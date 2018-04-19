from chatbot.actions import backend_api


class FakeResponse(object):
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


def test_get_all_employees(mocker):
    mock_request = mocker.patch('requests.get')
    mock_request.return_value = FakeResponse(200, {'name': 'foobar'})
    assert {'name': 'foobar'} == backend_api.get_employee('foo@bar')
    mock_request.assert_called_with('http://google.de/people/foo', headers={'Authorization': 'secret-token'})
