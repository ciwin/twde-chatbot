import datetime
import logging

from rasa_core.actions import Action

from chatbot.actions import employee
from chatbot.backend import leave_backend_api
from chatbot.backend.errors import BackendError

logger = logging.getLogger(__name__)


def get_annual_leave_total(employee_info, year):
    leave_details = leave_backend_api.get_leave_entitlement(employee_info, year)
    return leave_details.get('leaveEntitlement')


class ActionLeaveAnnualTotal(Action):
    def name(self):
        return 'action_leave_annual_total'

    def run(self, dispatcher, tracker, domain):
        employee_info = employee.get_employee(tracker.sender_id, dispatcher)
        if not employee_info:
            return []

        current_year = datetime.datetime.now().year

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
