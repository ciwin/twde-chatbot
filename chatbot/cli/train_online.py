#!/usr/bin/env python
import os

from rasa_core import utils
from rasa_core.channels.console import ConsoleInputChannel

from chatbot.nlp_models import dialog, intent_classificator


def run():
    classificator = intent_classificator.load_classificator()
    return dialog.train_dialog_online(classificator, ConsoleInputChannel())


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel=os.getenv('LOGLEVEL', 'ERROR'))
    run()
