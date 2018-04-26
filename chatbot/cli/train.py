#!/usr/bin/env python3
from chatbot.nlp_models import intent_classificator, dialog


def run():
    intent_classificator.train_classificator()
    dialog.train_dialog()


if __name__ == '__main__':
    run()
