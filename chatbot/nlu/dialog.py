import logging
import threading

from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.train import train_dialogue_model

from chatbot.config import Config
from chatbot.nlu import intent_classificator

logger = logging.getLogger(__name__)


_AGENT = None
_AGENT_LOCK = threading.RLock()


def get_agent():
    global _AGENT
    if not _AGENT:
        with _AGENT_LOCK:
            _AGENT = load_agent(intent_classificator.load_classificator())
    return _AGENT


def load_agent(intent_classificator):
    conf = Config()
    logger.info('loading context model from: %s', conf.get_value('dialog-model-path'))
    return Agent.load(conf.get_value('dialog-model-path'), interpreter=intent_classificator)


def handle_message_input(context_agent, user_input):
    responses = context_agent.handle_message(user_input)

    # FIXME: We chose the first one, not the best heuristic.
    # FIXME: Hardcoded fallback message.
    return responses[0] if responses else 'Sorry I cannot understand!'


def train_dialog():
    conf = Config()
    train_dialogue_model(conf.get_value('domain-file'), conf.get_value('stories-file'),
                         conf.get_value('dialog-model-path'))


def train_dialog_online(intent_classificator, input_channel):
    conf = Config()
    agent = Agent(conf.get_value('domain-file'), policies=[MemoizationPolicy(), KerasPolicy()],
                  interpreter=intent_classificator)

    agent.train_online(conf.get_value('stories-file'),
                       input_channel=input_channel,
                       max_history=conf.get_value('dialog-model-max-history'),
                       batch_size=conf.get_value('dialog-model-batch-size'),
                       epochs=conf.get_value('dialog-model-epochs'),
                       max_training_samples=conf.get_value('dialog-model-max-training-samples'))
    return agent
