import subprocess

from chatbot.cli import train
from chatbot.messenger import google_chat_api

from .. import helpers


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


def mock_external_systems(mocker):
    get_employee_mock = mocker.patch('chatbot.actions.backend_api.get_employee')
    get_employee_mock.return_value = {'employeeId': 'foobar', 'homeOffice': {'name': 'Berlin'},
                                      'preferredName': 'foo', 'unnecessary': 42}


with google_chat_api.app.test_client() as client:
    def test_ask_for_leave(mocker):
        mock_external_systems(mocker)
        helpers.conversation_tester(client, 'ask_for_leave.json')

    def test_check_leaves_and_holidays(mocker):
        mock_external_systems(mocker)
        helpers.conversation_tester(client, 'check_leaves_and_holidays.json')
