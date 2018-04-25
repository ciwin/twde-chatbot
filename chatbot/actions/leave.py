import datetime
import itertools
import logging
from functools import reduce

from rasa_core.actions import Action
from workalendar.registry import registry

from chatbot import session
from chatbot.actions import leave_backend_api, backend_api
from chatbot.actions.errors import BackendError

logger = logging.getLogger(__name__)
GERMANY_OFFICES = {
    'Berlin': 'DE-BE',
    'Hamburg': 'DE-HH',
    'Cologne': 'DE-NW',
    'Munich': 'DE-BY',
}
VALID_LEAVES = ['Annual Leave', 'Personal Development Leave']


def valid_user(employee):
    return employee and employee.get('homeOffice').get('name') in GERMANY_OFFICES


def get_annual_leave_total(employee, year):
    leave_details = leave_backend_api.get_leave_entitlement(employee, year)
    return leave_details.get('leaveEntitlement')


def _leave_is_within_year(leave, year):
    start_within_year = datetime.datetime.strptime(leave['period']['startsOn'], '%d-%m-%Y').year == year
    end_within_year = datetime.datetime.strptime(leave['period']['endsOn'], '%d-%m-%Y').year == year
    is_valid_leave = leave['type'] in VALID_LEAVES
    return is_valid_leave and (start_within_year or end_within_year)


def _leave_duration_days(leave, year):
    start = datetime.datetime.strptime(leave['period']['startsOn'], '%d-%m-%Y')
    if start.year < year:
        start = datetime.datetime(year, 1, 1)

    end = datetime.datetime.strptime(leave['period']['endsOn'], '%d-%m-%Y')
    if end.year > year:
        end = datetime.datetime(year, 12, 31)

    delta = (end - start)
    return delta.days + 1


def get_leaves_taken_(employee, year):
    valid_leaves = list(filter(lambda leave: _leave_is_within_year(leave, year),
                               backend_api.get_leaves(employee.get('employeeId'))))
    return reduce(lambda acc, leave: acc + _leave_duration_days(leave, year), valid_leaves, 0)


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

        try:
            total_annual_leaves = get_annual_leave_total(employee_info, current_year)
            dispatcher.utter_template(
                "utter_leave_annual_total",
                annual_total=total_annual_leaves,
                this_year=current_year,
            )
        except BackendError as ex:
            logger.warning("Leave Backend not available %s", ex)
            dispatcher.utter_template('utter_backend_not_running')

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


class ActionLeaveTaken(Action):
    def name(self):
        return 'action_leave_annual_taken'

    def run(self, dispatcher, tracker, domain):
        current_year = datetime.datetime.now().year

        employee_info = session.get_employee(tracker.sender_id)
        if not valid_user(employee_info):
            logger.warning("invalid user: %s:%s", tracker.sender_id, employee_info)
            dispatcher.utter_template("utter_invalid_user")
            return []

        try:
            taken_leaves = get_leaves_taken_(employee_info, current_year)
            dispatcher.utter_template(
                "utter_leave_annual_taken",
                taken_leaves=taken_leaves,
            )
        except BackendError as ex:
            logger.warning("Leave Backend not available %s", ex)
            dispatcher.utter_template('utter_backend_not_running')
