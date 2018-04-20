from rasa_core.interpreter import RasaNLUInterpreter
from chatbot.config import CONF
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer


def load_classificator():
    return RasaNLUInterpreter(CONF.get_value('classification-model-path'))


def train_classificator():
    trainer = Trainer(RasaNLUConfig(CONF.get_value('nlu-config-file-path')))
    training_data = load_data(CONF.get_value('nlu-training-data-path'))
    trainer.train(training_data)
    trainer.persist(CONF.get_value('models-directory'), fixed_model_name=CONF.get_value('classification-model-name'))
