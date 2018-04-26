import datetime
import itertools

from workalendar.registry import registry

from chatbot.actions.leave import GERMANY_OFFICES, LeaveBaseAction


def next_public_holiday(from_date, employee):
    state_code = GERMANY_OFFICES.get(employee['homeOffice']['name'])
    state_calendar = registry.get_calendar_class(state_code)()

    holidays = itertools.chain(state_calendar.holidays(from_date.year), state_calendar.holidays(from_date.year + 1))
    holidays = itertools.dropwhile(lambda d: d[0] <= from_date, holidays)
    return next(holidays)[0]


class ActionPublicHolidays(LeaveBaseAction):
    def name(self):
        return 'action_next_public_holiday'

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)

        today = datetime.date.today()

        next_holiday = next_public_holiday(today, self.employee_info)

        dispatcher.utter_template(
            "utter_public_holidays",
            date=next_holiday.strftime('%d %B %Y'),
        )

        return []
