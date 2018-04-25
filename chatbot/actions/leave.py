import datetime
import itertools
import logging

from rasa_core.actions import Action
from workalendar.registry import registry

from chatbot import session
from chatbot.actions import leave_backend_api

logger = logging.getLogger(__name__)
GERMANY_OFFICES = {
    'Berlin': 'DE-BE',
    'Hamburg': 'DE-HH',
    'Cologne': 'DE-NW',
    'Munich': 'DE-BY',
}


def valid_user(employee):
    return employee and employee.get('homeOffice').get('name') in GERMANY_OFFICES


def get_annual_leave_total(employee, year):
    leave_details = leave_backend_api.get_leave_entitlement(employee, year)
    return leave_details.get('leaveEntitlement')


class ActionLeaveAnnualTotal(Action):
    def name(self):
        return 'action_leave_annual_total'

    def run(self, dispatcher, tracker, domain):
        current_year = datetime.datetime.now().year

        employee_info = session.get_employee(tracker.sender_id)
        if not valid_user(employee_info):
            logger.warning("invalid user: %s:%s", tracker.sender_id, employee_info)
            dispatcher.utter_template("utter_invalid_user")
            return []

        total_annual_leaves = get_annual_leave_total(employee_info, current_year)
        dispatcher.utter_template(
            "utter_leave_annual_total",
            annual_total=total_annual_leaves,
            this_year=current_year,
        )

        return []


def next_public_holiday(from_date, employee):
    state_code = GERMANY_OFFICES.get(employee['homeOffice']['name'])
    state_calendar = registry.get_calendar_class(state_code)()

    holidays = itertools.chain(state_calendar.holidays(from_date.year), state_calendar.holidays(from_date.year + 1))
    holidays = itertools.dropwhile(lambda d: d[0] <= from_date, holidays)
    return next(holidays)[0]


class ActionPublicHolidays(Action):
    def name(self):
        return 'action_next_public_holiday'

    def run(self, dispatcher, tracker, domain):
        today = datetime.date.today()

        employee_info = session.get_employee(tracker.sender_id)
        if not valid_user(employee_info):
            logger.warning("invalid user: %s:%s", tracker.sender_id, employee_info)
            dispatcher.utter_template("utter_invalid_user")
            return []

        next_holiday = next_public_holiday(today, employee_info)

        dispatcher.utter_template(
            "utter_public_holidays",
            date=next_holiday.strftime('%d %B %Y'),
        )

        return []
