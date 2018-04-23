import logging
import time
import threading

from chatbase.base_message import Message, MessageSet

from chatbot.config import CONF


logger = logging.getLogger(__name__)

_MESSAGES = MessageSet(
    api_key=CONF.get_value('chatbase-api-key'),
)
_MESSAGES_LOCK = threading.RLock()


def _add_message(msg):
    with _MESSAGES_LOCK:
        _MESSAGES.append_message(msg)


def start_batch_sender():
    def background_task():
        interval = int(CONF.get_value('analytics-send-period'))
        while 1:
            logger.debug("send a batch of %d messages to chatbase and then sleep for %ds",
                         len(_MESSAGES.messages), interval)
            with _MESSAGES_LOCK:
                if _MESSAGES.messages:
                    response = _MESSAGES.send()
                    logger.debug("chatbat returned %s -> %s", response.status_code, response.content)
                    _MESSAGES.messages = []

            time.sleep(interval)

    t = threading.Thread(target=background_task)
    t.daemon = True
    t.start()


def send_user_message(msg, intent, sender_id):
    logger.debug('Send user message to chatbase msg=%s intent=%s sender_id=%s', msg, intent, sender_id)

    _add_message(Message(
        api_key=CONF.get_value('chatbase-api-key'),
        message=msg,
        type='user',
        platform='chatbot',
        intent=intent,
        user_id=sender_id,
    ))


def send_bot_message(msg, sender_id=None):
    logger.debug('Send bot message to chatbase msg=%s sender_id=%s', msg, sender_id)

    _add_message(Message(
        api_key=CONF.get_value('chatbase-api-key'),
        message=msg,
        type='agent',
        platform='chatbot',
        user_id=sender_id,
    ))


def send_not_handled_message(msg, sender_id=None):
    logger.debug('Send not handled message to chatbase msg=%s sender_id=%s', msg, sender_id)

    _add_message(Message(
        api_key=CONF.get_value('chatbase-api-key'),
        message=msg,
        user_id=sender_id,
        type='user',
        platform='chatbot',
        not_handled=True,
    ))
