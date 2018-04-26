import logging
import threading

from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter

from chatbot import analytics
from chatbot.config import CONF

logger = logging.getLogger(__name__)

_AGENT = None
_AGENT_LOCK = threading.RLock()


def load_classificator():
    return RasaNLUInterpreter(CONF.get_value('classification-model-path'))


def get_agent():
    global _AGENT
    if not _AGENT:
        logger.debug("Creating a new agent")
        with _AGENT_LOCK:
            _AGENT = load_agent(load_classificator())
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
