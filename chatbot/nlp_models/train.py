from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.train import train_dialogue_model
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Trainer

from chatbot.config import CONF


TRAINING_OPTIONS = {
    'max_history': CONF.get_value('dialog-model-max-history'),
    'batch_size': CONF.get_value('dialog-model-batch-size'),
    'epochs': CONF.get_value('dialog-model-epochs'),
    'max_training_samples': CONF.get_value('dialog-model-max-training-samples'),
}


def train_classificator():
    trainer = Trainer(RasaNLUConfig(CONF.get_value('nlu-config-file-path')))
    training_data = load_data(CONF.get_value('nlu-training-data-path'))
    trainer.train(training_data)
    trainer.persist(CONF.get_value('models-directory'), fixed_model_name=CONF.get_value('classification-model-name'))


def train_dialog():
    train_dialogue_model(
        CONF.get_value('domain-file'),
        CONF.get_value('stories-file'),
        CONF.get_value('dialog-model-path'),
        kwargs=TRAINING_OPTIONS,
    )


def train_dialog_online(classificator, input_channel):
    agent = Agent(CONF.get_value('domain-file'), policies=[MemoizationPolicy(), KerasPolicy()],
                  interpreter=classificator)

    agent.train_online(CONF.get_value('stories-file'),
                       input_channel=input_channel,
                       **TRAINING_OPTIONS)
    return agent
