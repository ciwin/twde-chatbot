from datetime import datetime, timedelta
from functools import reduce

from chatbot.actions.employee import GERMANY_OFFICES

from workalendar.registry import registry

HALF_DAY_LEAVE = 0.5
WHOLE_DAY_LEAVE = 1.0
DATE_FORMAT = '%d-%m-%Y'
VALID_LEAVES = ['Annual Leave', 'Personal Development Leave']


def total_leave_days(leave_records, office, year=None):
    valid_leaves = [
        leave
        for leave in leave_records
        if _is_valid_leave(leave, year)
    ]
    return reduce(lambda acc, leave: acc + _leave_duration_days(leave, office, year), valid_leaves, 0.0)


def _is_valid_leave(leave, year):
    is_valid_leave_type = leave['type'] in VALID_LEAVES
    if not year:
        return is_valid_leave_type

    start_within_year = datetime.strptime(leave['period']['startsOn'], DATE_FORMAT).year == year
    end_within_year = datetime.strptime(leave['period']['endsOn'], DATE_FORMAT).year == year

    return is_valid_leave_type and (start_within_year or end_within_year)


def _leave_duration_days(leave, office, year):
    leave_period = leave['period']
    start = datetime.strptime(leave_period['startsOn'], DATE_FORMAT)
    end = datetime.strptime(leave_period['endsOn'], DATE_FORMAT)
    if year and start.year < year:
        start = datetime(year, 1, 1)

    if year and end.year > year:
        end = datetime(year, 12, 31)

    work_calendar = registry.get_calendar_class(GERMANY_OFFICES.get(office))()
    leave_days = _calculate_duration_working_days(end, start, work_calendar)

    if leave_period['startsOnHalf'] and work_calendar.is_working_day(start):
        leave_days -= HALF_DAY_LEAVE

    if leave_period['endsOnHalf'] and work_calendar.is_working_day(end):
        leave_days -= HALF_DAY_LEAVE

    return leave_days


def _calculate_duration_working_days(end, start, work_calendar):
    days_in_leave_period = (end - start).days + 1
    day_generator = (start + timedelta(x) for x in range(days_in_leave_period))
    return sum(WHOLE_DAY_LEAVE for day in day_generator if work_calendar.is_working_day(day))
