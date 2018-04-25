import pytest

from chatbot.messenger import google_chat_api

from .. import helpers


SMOKE_CONVERSATIONS = [
    'ask_for_leave.json',
    'check_leaves_and_holidays.json',
]


with google_chat_api.app.test_client() as client:
    @pytest.mark.e2e
    def test_happy_path():
        for convfile in SMOKE_CONVERSATIONS:
            helpers.conversation_tester(client, convfile)
