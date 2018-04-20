import pytest

from chatbot.actions import leave
from chatbot.actions.errors import InvalidUserError


def test_valid_user():
    assert True is leave.valid_user({'homeOffice': {'name': 'Berlin'}})
    assert True is leave.valid_user({'homeOffice': {'name': 'Hamburg'}})
    assert True is leave.valid_user({'homeOffice': {'name': 'Munich'}})
    assert True is leave.valid_user({'homeOffice': {'name': 'Cologne'}})

    assert False is leave.valid_user({'homeOffice': {'name': 'Barcelona'}})
    assert False is leave.valid_user({'homeOffice': {'name': 'Antarctica'}})


def test_annual_leave():
    assert 28 == leave.get_annual_leave({'homeOffice': {'name': 'Berlin'}})
    assert 28 == leave.get_annual_leave({'homeOffice': {'name': 'Hamburg'}})
    assert 28 == leave.get_annual_leave({'homeOffice': {'name': 'Munich'}})
    assert 28 == leave.get_annual_leave({'homeOffice': {'name': 'Cologne'}})

    with pytest.raises(InvalidUserError) as error_info:
        leave.get_annual_leave({'homeOffice': {'name': 'Antarctica'}})
    assert 'Only german users allowed' in str(error_info.value)


def test_annual_leave_total(mocker):
    mocked_leave_api = mocker.patch('chatbot.actions.leave_backend_api.get_leave_adjustment')
    mocked_leave_api.return_value = 3

    assert 31 == leave.get_annual_leave_total({'employeeId': '42', 'homeOffice': {'name': 'Berlin'}}, 2018)
    mocked_leave_api.assert_called_with('42', 2018)

    with pytest.raises(InvalidUserError) as error_info:
        leave.get_annual_leave_total({'employeeId': '42', 'homeOffice': {'name': 'Antarctica'}}, 2018)
    assert 'Only german users allowed' in str(error_info.value)
