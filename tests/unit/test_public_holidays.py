import datetime

from chatbot.actions import public_holidays


def test_next_public_holiday():
    assert datetime.date(2018, 5, 1) == public_holidays.next_public_holiday(datetime.date(2018, 4, 24),
                                                                            {'employeeId': 42,
                                                                             'homeOffice': {'name': 'Berlin'}})

    assert datetime.date(2018, 5, 10) == public_holidays.next_public_holiday(datetime.date(2018, 5, 1),
                                                                             {'employeeId': 42,
                                                                              'homeOffice': {'name': 'Berlin'}})

    assert datetime.date(2019, 1, 1) == public_holidays.next_public_holiday(datetime.date(2018, 12, 31),
                                                                            {'employeeId': 42,
                                                                             'homeOffice': {'name': 'Berlin'}})
