import datetime
import logging

from rasa_core.actions import Action

from chatbot.actions import employee
from chatbot.actions import leave
from chatbot.backend import backend_api, leave_backend_api
from chatbot.backend.errors import BackendError

logger = logging.getLogger(__name__)


def get_leaves_taken(employee_info, year):
    office = employee_info['homeOffice']['name']
    leaves = backend_api.get_leaves(employee_info.get('employeeId'))
    return leave.total_leave_days(leaves, office, year)


def get_leaves_left(employee_info, year):
    leave_entitlement = leave_backend_api.get_leave_entitlement(employee_info, year)['leaveEntitlement']
    taken_leaves = get_leaves_taken(employee_info, year)
    return leave_entitlement - taken_leaves


class ActionLeaveTaken(Action):
    def name(self):
        return 'action_leave_annual_taken'

    def run(self, dispatcher, tracker, domain):
        employee_info = employee.get_employee(tracker.sender_id, dispatcher)
        if not employee_info:
            return []

        current_year = datetime.datetime.now().year

        try:
            taken_leaves = get_leaves_taken(employee_info, current_year)
            dispatcher.utter_template(
                "utter_leave_annual_taken",
                taken_leaves=taken_leaves,
            )
        except BackendError as ex:
            logger.warning("Leave Backend not available %s", ex)
            dispatcher.utter_template('utter_backend_not_running')


class ActionLeaveLeft(Action):
    def name(self):
        return 'action_leave_annual_left'

    def run(self, dispatcher, tracker, domain):
        employee_info = employee.get_employee(tracker.sender_id, dispatcher)
        if not employee_info:
            return []

        current_year = datetime.datetime.now().year

        try:
            days_left = get_leaves_left(employee_info, current_year)
            dispatcher.utter_template(
                "utter_leave_annual_left",
                days_left=days_left,
                year=current_year
            )
        except BackendError as ex:
            logger.warning("Leave Backend not available %s", ex)
            dispatcher.utter_template('utter_backend_not_running')
