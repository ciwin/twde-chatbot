import datetime
import itertools
import json
import os
import subprocess

from freezegun import freeze_time

from chatbot.cli import train
from chatbot.messenger import google_chat_api
from chatbot.nlu import dialog

MODULE_PATH = os.path.abspath(os.path.join(__file__, '..'))

google_chat_api.app.testing = True


def teardown_module(_):
    from chatbot.session import _get_client
    _get_client().flushdb()

    from chatbot.session import _reset_client
    _reset_client()


def setup_module(_):
    # FIXME: This take quite some time.
    commands = [
        "python -m spacy download en_core_web_md",
        "python -m spacy link --force en_core_web_md en",
    ]
    for cmd in commands:
        subprocess.call(cmd, shell=True)

    train.run()


def get_body(message, func_name):
    return {
        'token': 'secret-api-key',
        'type': 'MESSAGE',
        'message': {
            'text': message,
            'sender': {
                'email': 'foo@bar.com',
            },
            'thread': {
                'name': 'foo/thread/{}'.format(func_name),
            }
        },
    }


def mock_external_systems(mocker):
    get_employee_mock = mocker.patch('chatbot.actions.backend_api.get_employee')
    get_employee_mock.return_value = {'employeeId': 'foobar', 'homeOffice': {'name': 'Berlin'},
                                      'preferredName': 'foo', 'unnecessary': 42}


def get_templates(name):
    agent = dialog.get_agent()
    return [t['text'] for t in agent.domain.templates[name]]


@freeze_time("2018-04-24")
def conversation_tester(mocking_system, conversational_file):
    mock_external_systems(mocking_system)

    with open(os.path.join(MODULE_PATH, 'fixtures/conversations/' + conversational_file)) as fp:
        testcases = json.load(fp)

    for input, output in testcases.items():
        body = get_body(input, conversational_file)
        response = client.post('/endpoint', data=json.dumps(body),
                               content_type='application/json')

        assert 200 == response.status_code

        parsed_response = json.loads(response.data)

        messages = [get_templates(name) for name in output['templates']]
        expected_responses = ["\n".join(opts) for opts in itertools.product(*messages)]

        # Fill placeholders.
        expected_responses = [resp.format(date=datetime.date(2018, 5, 1).strftime("%d %B %Y")) for resp in expected_responses]

        assert parsed_response["text"] in expected_responses, "fails for '{}'".format(input)


with google_chat_api.app.test_client() as client:
    def test_ask_for_leave(mocker):
        conversation_tester(mocker, 'ask_for_leave.json')


    def test_check_leaves_and_holidays(mocker):
        conversation_tester(mocker, 'check_leaves_and_holidays.json')
