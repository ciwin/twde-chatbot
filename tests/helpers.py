import datetime
import itertools
import json
import os

from freezegun import freeze_time

from chatbot.nlu import dialog

MODULE_PATH = os.path.abspath(os.path.join(__file__, '..'))


def get_body(message, thread_name):
    return {
        'token': 'secret-api-key',
        'type': 'MESSAGE',
        'message': {
            'text': message,
            'sender': {
                'email': 'foo@bar.com',
            },
            'thread': {
                'name': 'tests/thread/{}'.format(thread_name),
            }
        },
    }


@freeze_time("2018-04-24")
def conversation_tester(client, conversational_file):
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
        expected_responses = [
            resp.format(date=datetime.date(2018, 5, 1).strftime("%d %B %Y")) for resp in expected_responses
        ]

        assert parsed_response["text"] in expected_responses, "fails for '{}'".format(input)


def get_templates(name):
    agent = dialog.get_agent()
    return [t['text'] for t in agent.domain.templates[name]]


class FakeResponse(object):
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data
