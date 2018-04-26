import datetime
import logging

from chatbot.actions import leave_backend_api
from chatbot.actions.errors import BackendError
from chatbot.actions.leave import LeaveBaseAction

logger = logging.getLogger(__name__)


def get_annual_leave_total(employee, year):
    leave_details = leave_backend_api.get_leave_entitlement(employee, year)
    return leave_details.get('leaveEntitlement')


class ActionLeaveAnnualTotal(LeaveBaseAction):
    def name(self):
        return 'action_leave_annual_total'

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
        current_year = datetime.datetime.now().year

        try:
            total_annual_leaves = get_annual_leave_total(self.employee_info, current_year)
            dispatcher.utter_template(
                "utter_leave_annual_total",
                annual_total=total_annual_leaves,
                this_year=current_year,
            )
        except BackendError as ex:
            logger.warning("Leave Backend not available %s", ex)
            dispatcher.utter_template('utter_backend_not_running')

        return []
