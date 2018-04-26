import datetime
import itertools

from rasa_core.actions import Action
from workalendar.registry import registry

from chatbot.actions import employee
from chatbot.actions.employee import GERMANY_OFFICES


def next_public_holiday(from_date, employee_info):
    state_code = GERMANY_OFFICES.get(employee_info['homeOffice']['name'])
    state_calendar = registry.get_calendar_class(state_code)()

    holidays = itertools.chain(state_calendar.holidays(from_date.year), state_calendar.holidays(from_date.year + 1))
    holidays = itertools.dropwhile(lambda d: d[0] <= from_date, holidays)
    return next(holidays)[0]


class ActionPublicHolidays(Action):
    def name(self):
        return 'action_next_public_holiday'

    def run(self, dispatcher, tracker, domain):
        employee_info = employee.get_employee(tracker.sender_id, dispatcher)
        if not employee_info:
            return []

        today = datetime.date.today()

        next_holiday = next_public_holiday(today, employee_info)

        dispatcher.utter_template(
            "utter_public_holidays",
            date=next_holiday.strftime('%d %B %Y'),
        )

        return []
