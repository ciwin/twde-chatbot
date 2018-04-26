import logging

from chatbot import session

logger = logging.getLogger(__name__)
GERMANY_OFFICES = {
    'Berlin': 'DE-BE',
    'Hamburg': 'DE-HH',
    'Cologne': 'DE-NW',
    'Munich': 'DE-BY',
}


def _valid_user(employee):
    return employee and employee.get('homeOffice').get('name') in GERMANY_OFFICES


def get_employee(sender_id, dispatcher):
    employee_info = session.get_employee(sender_id)
    if not employee_info:
        logger.warning("invalid user: %s:%s", sender_id, employee_info)
        dispatcher.utter_template("utter_invalid_user")
        return

    home_office = employee_info.get('homeOffice').get('name')
    if home_office not in GERMANY_OFFICES:
        dispatcher.utter_template(
            "utter_unsupported_office",
            home_office=home_office,
        )
        return

    return employee_info
