from chatbot.actions import taken_leaves


def test_leaves_taken_within_same_year(mocker):
    leave_days_calculator_mock = mocker.patch('chatbot.actions.leave.total_leave_days')
    leave_days_calculator_mock.return_value = 3
    leave_api_mock = mocker.patch('chatbot.backend.leave_backend_api.get_leave_entitlement')
    leave_api_mock.return_value = {'leaveEntitlement': 42}
    backend_mock = mocker.patch('chatbot.backend.backend_api.get_leaves')
    backend_mock.return_value =  [
        {
            "id": "16487",
            "type": "Annual Leave",
            "period": {
                "startsOn": "25-05-2018",
                "startsOnHalf": False,
                "endsOn": "25-05-2018",
                "endsOnHalf": False
            }
        },
        {
            "id": "16344",
            "type": "Personal Development Leave",
            "period": {
                "startsOn": "15-02-2018",
                "startsOnHalf": False,
                "endsOn": "16-02-2018",
                "endsOnHalf": False
            }
        },
        {
            "id": "16345",
            "type": "foo",
            "period": {
                "startsOn": "13-02-2018",
                "startsOnHalf": False,
                "endsOn": "14-02-2018",
                "endsOnHalf": False
            }
        }
    ]

    assert 3 == taken_leaves.get_leaves_taken({'employeeId': '42', 'homeOffice': {'name': 'Berlin'}}, 2018)
    assert 42 - 3 == taken_leaves.get_leaves_left({'employeeId': '42', 'homeOffice': {'name': 'Berlin'}}, 2018)
    leave_days_calculator_mock.assert_called_with(backend_mock.return_value, 'Berlin', 2018)
