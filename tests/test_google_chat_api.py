from flask import json

from chatbot.messenger import google_chat_api

google_chat_api.app.testing = True

with google_chat_api.app.test_client() as client:
    def test_sending_bad_request():
        response = client.post('/endpoint')

        assert 400 == response.status_code

        parsed_response = json.loads(response.data)
        assert "Bad request" == parsed_response["error"]


    def test_sending_invalid_token():
        response = client.post('/endpoint', data=json.dumps(dict(foo='bar')), content_type='application/json')

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
        response = client.post('/endpoint', data=json.dumps(dict(token='secret-api-key',
                                                                 space='some space',
                                                                 type='MESSAGE',
                                                                 message=dict(text='some message',
                                                                              thread=dict(name='id1'))),
                               content_type='application/json')

        assert 200 == response.status_code

        parsed_response = json.loads(response.data)
        assert "I was called" == parsed_response["text"]
