import logging
import threading

from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.train import train_dialogue_model

from chatbot import analytics
from chatbot.config import CONF
from chatbot.nlu import intent_classificator

logger = logging.getLogger(__name__)

_AGENT = None
_AGENT_LOCK = threading.RLock()


def get_agent():
    global _AGENT
    if not _AGENT:
        logger.debug("Creating a new agent")
        with _AGENT_LOCK:
            _AGENT = load_agent(intent_classificator.load_classificator())
    return _AGENT


def load_agent(classificator):
    logger.info('loading context model from: %s', CONF.get_value('dialog-model-path'))
    return Agent.load(CONF.get_value('dialog-model-path'), interpreter=classificator)


def handle_message_input(context_agent, user_input, sender_id=None):
    responses = context_agent.handle_message(user_input, sender_id=sender_id)

    if responses:
        parsed_data = context_agent.interpreter.parse(user_input)
        analytics.send_user_message(user_input, parsed_data.get('intent', {})['name'], sender_id)
    else:
        analytics.send_not_handled_message(user_input, sender_id)

    reply = '\n'.join(responses) if responses else get_fallback_message(context_agent)
    analytics.send_bot_message(reply, sender_id=sender_id)
    return reply


def get_welcome_message(context_agent, sender_id=None):
    msg = context_agent.domain.random_template_for('utter_welcome')['text']
    analytics.send_bot_message(msg, sender_id=sender_id)
    return msg


def get_fallback_message(context_agent):
    return context_agent.domain.random_template_for('utter_fallback')['text']


def train_dialog():
    train_dialogue_model(CONF.get_value('domain-file'), CONF.get_value('stories-file'),
                         CONF.get_value('dialog-model-path'))


def train_dialog_online(classificator, input_channel):
    agent = Agent(CONF.get_value('domain-file'), policies=[MemoizationPolicy(), KerasPolicy()],
                  interpreter=classificator)

    agent.train_online(CONF.get_value('stories-file'),
                       input_channel=input_channel,
                       max_history=CONF.get_value('dialog-model-max-history'),
                       batch_size=CONF.get_value('dialog-model-batch-size'),
                       epochs=CONF.get_value('dialog-model-epochs'),
                       max_training_samples=CONF.get_value('dialog-model-max-training-samples'))
    return agent
