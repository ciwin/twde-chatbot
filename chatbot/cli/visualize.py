#!/usr/bin/env python
import sys

try:
    import graphviz  # noqa
except ImportError:
    print("error: graphviz is not installed")
    print("For OSX please run: brew install graphviz")
    sys.exit(1)

from chatbot.nlu import dialog
from chatbot.config import CONF


def run():
    output_file = "/tmp/graph.png"
    stories_file = CONF.get_value('stories-file')
    agent = dialog.get_agent()

    agent.visualize(stories_file,
                    output_file=output_file, max_history=2)

    print("File generated: {}".format(output_file))


if __name__ == '__main__':
    run()
