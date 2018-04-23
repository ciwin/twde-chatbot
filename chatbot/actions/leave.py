import datetime
import logging

from rasa_core.actions import Action

from chatbot import session
from chatbot.actions import leave_backend_api

logger = logging.getLogger(__name__)
GERMANY_OFFICES = ['Berlin', 'Hamburg', 'Cologne', 'Munich']
ANNUAL_BASE_LEAVE = 28


def valid_user(employee):
    return employee and employee.get('homeOffice').get('name') in GERMANY_OFFICES


def get_annual_leave_total(employee, year):
    leave_adjustments = leave_backend_api.get_leave_adjustment(employee.get('employeeId'), year)
    return ANNUAL_BASE_LEAVE + leave_adjustments


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
