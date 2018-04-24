from chatbot.actions import leave


def test_valid_user():
    assert True is leave.valid_user({'homeOffice': {'name': 'Berlin'}})
    assert True is leave.valid_user({'homeOffice': {'name': 'Hamburg'}})
    assert True is leave.valid_user({'homeOffice': {'name': 'Munich'}})
    assert True is leave.valid_user({'homeOffice': {'name': 'Cologne'}})

    assert False is leave.valid_user({'homeOffice': {'name': 'Barcelona'}})
    assert False is leave.valid_user({'homeOffice': {'name': 'Antarctica'}})


def test_annual_leave_total(mocker):
    mocked_leave_api = mocker.patch('chatbot.actions.leave_backend_api.get_leave_entitlement')
    mocked_leave_api.return_value = {'employeeId': '42', 'homeOffice':'Berlin', 'year': 2018, 'leaveEntitlement': 42}
    employee = {'employeeId': '42', 'homeOffice': {'name': 'Berlin'}}
    assert 42 == leave.get_annual_leave_total(employee, 2018)
    mocked_leave_api.assert_called_with(employee, 2018)
