import logging

from rasa_core.actions import Action

from chatbot import session

logger = logging.getLogger(__name__)
GERMANY_OFFICES = {
    'Berlin': 'DE-BE',
    'Hamburg': 'DE-HH',
    'Cologne': 'DE-NW',
    'Munich': 'DE-BY',
}


def valid_user(employee):
    return employee and employee.get('homeOffice').get('name') in GERMANY_OFFICES


class LeaveBaseAction(Action):
    def __init__(self):
        self.employee_info = None

    def name(self):
        pass

    def run(self, dispatcher, tracker, domain):
        self.employee_info = session.get_employee(tracker.sender_id)
        if not valid_user(self.employee_info):
            logger.warning("invalid user: %s:%s", tracker.sender_id, self.employee_info)
            dispatcher.utter_template("utter_invalid_user")
            return []
