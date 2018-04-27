from chatbot.actions import planned_leaves
from freezegun import freeze_time


@freeze_time("2018-04-27")
def test_should_only_cover_annual_leave_and_personal_development_leave(mocker):
    backend_mock = mocker.patch('chatbot.backend.backend_api.get_leaves')
    backend_mock.return_value = [
        {
            'type': 'Annual Leave',
            'period': {
                'startsOn': '28-05-2018',
                'startsOnHalf': False,
                'endsOn': '31-05-2018',
                'endsOnHalf': True
            }
        }
    ]

    leave_calculator_mock = mocker.patch('chatbot.actions.leave.total_leave_days')
    leave_calculator_mock.return_value = 3.5

    employee_info = {'employeeId': '42', 'homeOffice': {'name': 'Hamburg'}}

    assert 3.5 == planned_leaves.get_planned_leaves(employee_info)
    leave_calculator_mock.assert_called_with(backend_mock.return_value, 'Hamburg')
    backend_mock.assert_called_with('42', "27-04-2018")
