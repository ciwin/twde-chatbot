import datetime
import os
import subprocess

from freezegun import freeze_time

from chatbot.channels import google_chat_api
from chatbot.cli import train
from .. import helpers

google_chat_api.app.testing = True


def teardown_module(_):
    from chatbot.session import _get_client
    _get_client().flushdb()

    from chatbot.session import _reset_client
    _reset_client()


def setup_module(_):
    # FIXME: This take quite some time.
    if os.getenv('RUN_TRAINING') != 'n':
        train.run()


def mock_external_systems(mocker):
    get_employee_mock = mocker.patch('chatbot.backend.backend_api.get_employee')
    get_employee_mock.return_value = {'employeeId': 'foobar', 'homeOffice': {'name': 'Berlin'},
                                      'preferredName': 'foo'}

    leave_api_mock = mocker.patch('chatbot.backend.leave_backend_api.get_leave_entitlement')
    leave_api_mock.return_value = {'leaveEntitlement': 42}

    backend_mock = mocker.patch('chatbot.backend.backend_api.get_leaves')
    backend_mock.return_value = [
        {
            "id": "16487",
            "type": "Annual Leave",
            "period": {
                "startsOn": "25-05-2018",
                "startsOnHalf": False,
                "endsOn": "25-05-2018",
                "endsOnHalf": False
            }
        },
        {
            "id": "16344",
            "type": "Personal Development Leave",
            "period": {
                "startsOn": "16-02-2018",
                "startsOnHalf": False,
                "endsOn": "17-02-2018",
                "endsOnHalf": False
            }
        },
        {
            "id": "16345",
            "type": "foo",
            "period": {
                "startsOn": "13-02-2018",
                "startsOnHalf": False,
                "endsOn": "14-02-2018",
                "endsOnHalf": False
            }
        }
    ]


with google_chat_api.app.test_client() as client:
    @freeze_time("2018-04-24")
    def test_ask_for_leave(mocker):
        mock_external_systems(mocker)
        helpers.conversation_tester(
            client, 'ask_for_leave.json',
            template_filler={
                'days_left': 39,
                'year': 2018,
                'date': datetime.date(2018, 5, 1).strftime("%d %B %Y"),
            },
        )


    @freeze_time("2018-04-24")
    def test_check_leaves_and_holidays(mocker):
        mock_external_systems(mocker)
        helpers.conversation_tester(
            client, 'check_leaves_and_holidays.json',
            template_filler={
                'days_left': 39,
                'year': 2018,
                'date': datetime.date(2018, 5, 1).strftime("%d %B %Y"),
            },
        )
