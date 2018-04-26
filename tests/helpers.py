import itertools
import json
import os

from chatbot.nlp_models import dialog

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


def conversation_tester(client, conversational_file, template_filler):
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
            resp.format(**template_filler) for resp in expected_responses
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
