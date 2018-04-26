web: ./chatbot/cli/train.py && gunicorn --timeout=190 --workers=1 -k=gevent chatbot.cli.server:app
