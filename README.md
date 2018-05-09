[![CircleCI](https://circleci.com/gh/ThoughtWorksInc/twde-chatbot.svg?style=svg)](https://circleci.com/gh/ThoughtWorksInc/twde-chatbot)

# Chatbot
This chatbot uses [Rasa](http://rasa.com/).

## Documentation
Right now the documentation only contains interesting links to get started with [docs](https://github.com/ThoughtWorksInc/twde-chatbot/tree/master/docs)

## Installation

### Prerequisite

Make sure that:

- You have python3.
- [pipenv](https://docs.pipenv.org/) is installed, if not run `pip install pipenv`.
- Language setup correctly to english
```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

### Install

#### System Depdendencies

Make sure that graphviz is installed, in OSX that will be:

```bash
brew install pkg-config graphviz
```

#### Python Dependencies

To install all dependencies execute:

```
pipenv install --dev
```

## Play

### Training

First you need to train the bot, to do start by downloading language dependencies (this only need to be done once):

```
pipenv run python -m spacy download en_core_web_md
pipenv run python -m spacy link en_core_web_md en
```

Then run training use:

- `pipenv run chatbot/cli/train.py` for running normal training.
- `pipenv run chatbot/cli/train_online.py` for running interactive training.

### Running

First make sure that redis is running locally, one way of doing it is by running:

```bash
docker run --publish 6379:6379 --name redis -d redis
```

Then to start the bot there is multiple ways:

- In the console: ```pipenv run chatbot/cli/console.py```
- As a google chat api: ```pipenv run chatbot/cli/server.py```
- As a google chat api using Heroku: ```pipenv run heroku local```

To reduce logging verbosity set the environment variable LOGLEVEL to error, for example:

```
LOGLEVEL=ERROR pipenv run chatbot/cli/console.py
```

## Test

### Automated Testing

To run tests use:

```bash
pipenv run pytest
```

### Manual Testing

You need to send a POST to the following endpoint `http://localhost:5000/endpoint`, the body should conforms to
what Google Chat send, for more information about the payload check `tests/helpers.py` file for example of payload.

Another way to test will be to create a test bot in Google Chat, you can more information about how to do that [here](https://developers.google.com/hangouts/chat/concepts/bots).

Also you can use [ngrok](https://ngrok.com/) to expose a public address and use that in the bot configuration, just make sure that you set the `HANGOUT_API_KEY` environment variable to the same value that Google Chat provides. 
