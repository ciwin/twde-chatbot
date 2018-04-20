import datetime

from chatbot.actions import leave_backend_api
from chatbot.actions.errors import InvalidUserError

GERMANY = ['Berlin', 'Hamburg', 'Cologne', 'Munich']


def valid_user(user):
    return user.get('homeOffice') in GERMANY


def get_annual_leave(user):
    if valid_user(user):
        return 28
    else:
        raise InvalidUserError("Only german users allowed")


def get_annual_leave_total(user):
    current_year = datetime.datetime.now().year
    leave_adjustments = leave_backend_api.get_leave_adjustment(user.get('employeeId'), current_year)
    return get_annual_leave(user) + leave_adjustments
