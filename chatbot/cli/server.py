#!/usr/bin/env python3
import os
import threading

from werkzeug.contrib.profiler import ProfilerMiddleware

from chatbot.messenger import google_chat_api
from chatbot.nlu import dialog


app = google_chat_api.app
if os.getenv('FLASK_PROFILE'):
    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])


def _preload():
    # Run loading agent in background to not hold app from starting
    # since Heroku timeout and kill app if it doesn't listen after
    # some timeout.
    threading.Thread(target=dialog.get_agent).start()


def run():
    _preload()

    port = os.environ.get('PORT', 8080)
    app.run(port=port, debug=True)


if __name__ == '__main__':
    run()
