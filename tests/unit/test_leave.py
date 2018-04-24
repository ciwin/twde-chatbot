import datetime

from chatbot.actions import leave


def test_valid_user():
    assert True is leave.valid_user({'homeOffice': {'name': 'Berlin'}})
    assert True is leave.valid_user({'homeOffice': {'name': 'Hamburg'}})
    assert True is leave.valid_user({'homeOffice': {'name': 'Munich'}})
    assert True is leave.valid_user({'homeOffice': {'name': 'Cologne'}})

    assert False is leave.valid_user({'homeOffice': {'name': 'Barcelona'}})
    assert False is leave.valid_user({'homeOffice': {'name': 'Antarctica'}})


def test_annual_leave_total(mocker):
    mocked_leave_api = mocker.patch('chatbot.actions.leave_backend_api.get_leave_adjustment')
    mocked_leave_api.return_value = 3

    assert 31 == leave.get_annual_leave_total({'employeeId': '42', 'homeOffice': {'name': 'Berlin'}}, 2018)
    mocked_leave_api.assert_called_with('42', 2018)


def test_next_public_holiday():
    assert datetime.date(2018, 5, 1) == leave.next_public_holiday(datetime.date(2018, 4, 24),
                                                                  {'employeeId': 42, 'homeOffice': {'name': 'Berlin'}})

    assert datetime.date(2018, 5, 10) == leave.next_public_holiday(datetime.date(2018, 5, 1),
                                                                   {'employeeId': 42, 'homeOffice': {'name': 'Berlin'}})

    assert datetime.date(2019, 1, 1) == leave.next_public_holiday(datetime.date(2018, 12, 31),
                                                                  {'employeeId': 42, 'homeOffice': {'name': 'Berlin'}})