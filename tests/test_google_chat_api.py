from flask import json

from chatbot.messenger import google_chat_api

google_chat_api.app.testing = True

with google_chat_api.app.test_client() as client:
    def test_sending_non_json_request():
        response = client.post('/endpoint')

        assert 400 == response.status_code

        parsed_response = json.loads(response.data)
        assert "request is not JSON" == parsed_response["error"]

    def test_sending_invalid_token():
        response = client.post('/endpoint', data=json.dumps({'foo': 'bar'}), content_type='application/json')

        assert 401 == response.status_code

        parsed_response = json.loads(response.data)
        assert "Wrong token" == parsed_response["error"]

        response = client.post('/endpoint', data=json.dumps(dict(token='foobar')), content_type='application/json')

        assert 401 == response.status_code

        parsed_response = json.loads(response.data)
        assert "Wrong token" == parsed_response["error"]

    def test_sending_valid_token(mocker):
        mocker.patch('chatbot.nlu.dialog.get_agent')
        mocked_function = mocker.patch('chatbot.nlu.dialog.handle_message_input')
        mocked_function.return_value = "I was called"

        body = {
            'token': 'secret-api-key',
            'type': 'MESSAGE',
            'message': {
                'text': 'some message',
                'thread': {
                    'name': 'thread-name',
                }
            },
        }

        response = client.post('/endpoint', data=json.dumps(body),
                               content_type='application/json')

        assert 200 == response.status_code

        parsed_response = json.loads(response.data)
        assert "I was called" == parsed_response["text"]

    def test_get_welcome_message(mocker):
        mocker.patch('chatbot.nlu.dialog.get_agent')
        mocked_function = mocker.patch('chatbot.nlu.dialog.get_welcome_message')
        mocked_function.return_value = 'Welcome!'

        body = {
            'token': 'secret-api-key',
            'type': 'ADDED_TO_SPACE',
        }

        response = client.post('/endpoint', data=json.dumps(body),
                               content_type='application/json')

        assert 200 == response.status_code

        parsed_response = json.loads(response.data)
        assert "Welcome!" == parsed_response["text"]
