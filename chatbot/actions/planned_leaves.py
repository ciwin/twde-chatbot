from datetime import date

from rasa_core.actions import Action

from chatbot.actions import employee
from chatbot.actions import leave
from chatbot.backend import backend_api


def get_planned_leaves(employee_info):
    planned_leaves = backend_api.get_leaves(employee_info.get('employeeId'), f'{date.today():%d-%m-%Y}')
    return leave.total_leave_days(planned_leaves, employee_info['homeOffice']['name'])


class ActionAnnualLeavePlanned(Action):
    def name(self):
        return 'action_leave_annual_planned'

    def run(self, dispatcher, tracker, domain):
        employee_info = employee.get_employee(tracker.sender_id, dispatcher)
        if not employee_info:
            return []

        leaves_planned = get_planned_leaves(employee_info)

        dispatcher.utter_template(
            "utter_leave_annual_planned",
            leaves_planned=leaves_planned
        )

        return []
