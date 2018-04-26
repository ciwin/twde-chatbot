#!/usr/bin/env python
import pprint

from chatbot.config import CONF

from rasa_core.interpreter import RasaNLUInterpreter


interpreter = RasaNLUInterpreter(CONF.get_value('classification-model-path'))

while 1:
    text = input('Enter text: ')
    pprint.pprint(interpreter.parse(text))