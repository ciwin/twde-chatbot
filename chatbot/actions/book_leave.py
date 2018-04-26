import duckling
from rasa_core.actions import Action

from chatbot.actions import employee


class ActionBookLeave(Action):

    def __init__(self):
        self.__duckling_wrapper = None

    @property
    def duckling(self):
        if not self.__duckling_wrapper:
            self.__duckling_wrapper = duckling.DucklingWrapper()
        return self.__duckling_wrapper

    def name(self):
        return "action_book_leave"

    def run(self, dispatcher, tracker, domain):
        employee_info = employee.get_employee(tracker.sender_id, dispatcher)
        if not employee_info:
            return []

        leave_start_date = tracker.get_slot("leave_start_date")
        leave_end_date = tracker.get_slot("leave_end_date")

        print(">>>>> ", "Booking leave")
        print("####  leave_start_date: ", self.duckling.parse(leave_start_date))
        print("####  leave_end_date: ", self.duckling.parse(leave_end_date))
        return []
