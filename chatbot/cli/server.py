#!/usr/bin/env python3
import logging
import os
import threading
import time

from werkzeug.contrib.profiler import ProfilerMiddleware

from chatbot.analytics import start_batch_sender
from chatbot.config import CONF
from chatbot.messenger import google_chat_api
from chatbot.nlp_models import dialog

logger = logging.getLogger(__name__)


def _warmup():
    # Run loading get_agent in a loop to avoid having Heroku sleep
    # the process.
    def background_task():
        while 1:
            logger.debug("loading agent ...")
            dialog.get_agent()

            interval = int(CONF.get_value('warming-up-agent-interval'))
            time.sleep(interval)
    t = threading.Thread(target=background_task)
    t.daemon = True
    t.start()


_warmup()
start_batch_sender()
app = google_chat_api.app
if os.getenv('FLASK_PROFILE'):
    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])


def run():
    port = os.environ.get('PORT', 8080)
    app.run(port=port, debug=True)


if __name__ == '__main__':
    run()
