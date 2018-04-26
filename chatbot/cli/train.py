#!/usr/bin/env python3
from chatbot.nlp_models import train


def run():
    train.train_classificator()
    train.train_dialog()


if __name__ == '__main__':
    run()
