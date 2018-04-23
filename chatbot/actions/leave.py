import datetime
import logging

from rasa_core.actions import Action

from chatbot.actions import leave_backend_api
from chatbot.actions.errors import InvalidUserError, BackendError
from chatbot import session

GERMANY = ['Berlin', 'Hamburg', 'Cologne', 'Munich']
logger = logging.getLogger(__name__)


def valid_user(employee):
    return employee.get('homeOffice').get('name') in GERMANY


def get_annual_leave(employee):
    if valid_user(employee):
        return 28
    else:
        raise InvalidUserError("Only german users allowed")


def get_annual_leave_total(employee, year):
    leave_adjustments = leave_backend_api.get_leave_adjustment(employee.get('employeeId'), year)
    return get_annual_leave(employee) + leave_adjustments


class ActionLeaveAnnualTotal(Action):
    def name(self):
        return 'action_leave_annual_total'

    def run(self, dispatcher, tracker, domain):
        try:
            current_year = datetime.datetime.now().year

            employee_info = session.get_employee(tracker.sender_id)

            total_annual_leaves = get_annual_leave_total(employee_info, current_year)
            dispatcher.utter_template(
                "utter_leave_annual_total",
                annual_total=total_annual_leaves,
                this_year=current_year,
            )
        except BackendError as e:
            # TODO get this from utters
            logger.debug(e)
            dispatcher.utter_message("The backend is not responding :(")
        except InvalidUserError as e:
            # TODO get this from utters
            logger.debug(e)
            dispatcher.utter_message("You are not allowed to do anything")

        return []
