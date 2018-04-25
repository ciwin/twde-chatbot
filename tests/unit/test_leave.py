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
    mocked_leave_api = mocker.patch('chatbot.actions.leave_backend_api.get_leave_entitlement')
    mocked_leave_api.return_value = {'employeeId': '42', 'homeOffice': 'Berlin', 'year': 2018, 'leaveEntitlement': 42}
    employee = {'employeeId': '42', 'homeOffice': {'name': 'Berlin'}}
    assert 42 == leave.get_annual_leave_total(employee, 2018)
    mocked_leave_api.assert_called_with(employee, 2018)


def test_next_public_holiday():
    assert datetime.date(2018, 5, 1) == leave.next_public_holiday(datetime.date(2018, 4, 24),
                                                                  {'employeeId': 42, 'homeOffice': {'name': 'Berlin'}})

    assert datetime.date(2018, 5, 10) == leave.next_public_holiday(datetime.date(2018, 5, 1),
                                                                   {'employeeId': 42, 'homeOffice': {'name': 'Berlin'}})

    assert datetime.date(2019, 1, 1) == leave.next_public_holiday(datetime.date(2018, 12, 31),
                                                                  {'employeeId': 42, 'homeOffice': {'name': 'Berlin'}})


def test_leaves_taken_within_same_year(mocker):
    backend_mock = mocker.patch('chatbot.actions.backend_api.get_leaves')
    backend_mock.return_value = [
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
                "startsOn": "16-02-2018",
                "startsOnHalf": False,
                "endsOn": "17-02-2018",
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

    assert 1 + 2 == leave.get_leaves_taken_({'employeeId': '42', 'homeOffice': {'name': 'Berlin'}}, 2018)


def test_leaves_taken_with_different_years(mocker):
    backend_mock = mocker.patch('chatbot.actions.backend_api.get_leaves')
    backend_mock.return_value = [
        {
            "id": "16489",
            "type": "Annual Leave",
            "period": {
                "startsOn": "31-12-2017",
                "startsOnHalf": False,
                "endsOn": "02-01-2018",
                "endsOnHalf": False
            }
        },
        {
            "id": "16477",
            "type": "Annual Leave",
            "period": {
                "startsOn": "29-12-2018",
                "startsOnHalf": False,
                "endsOn": "02-01-2019",
                "endsOnHalf": False
            }
        }]

    assert 2 + 3 == leave.get_leaves_taken_({'employeeId': '42', 'homeOffice': {'name': 'Berlin'}}, 2018)
