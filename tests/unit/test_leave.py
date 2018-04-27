from chatbot.actions import leave


def test_should_only_cover_annual_leave_and_personal_development_leave():
    leaves = [
        {
            'type': 'Sick Leave',
            'period': {
                'startsOn': '02-05-2018',
                'startsOnHalf': False,
                'endsOn': '03-05-2018',
                'endsOnHalf': False
            }
        },
        {
            'type': 'Annual Leave',
            'period': {
                'startsOn': '07-05-2018',
                'startsOnHalf': False,
                'endsOn': '08-05-2018',
                'endsOnHalf': False
            }
        },
        {
            'type': 'Personal Development Leave',
            'period': {
                'startsOn': '14-05-2018',
                'startsOnHalf': False,
                'endsOn': '15-05-2018',
                'endsOnHalf': False
            }
        }
    ]

    assert 2.0 + 2.0 == leave.total_leave_days(leaves, 'Hamburg')


def test_should_minus_half_day_if_starts_on_half_day():
    leaves = [
        {
            'type': 'Annual Leave',
            'period': {
                'startsOn': '28-05-2018',
                'startsOnHalf': True,
                'endsOn': '31-05-2018',
                'endsOnHalf': False
            }
        }
    ]

    assert 4 - 0.5 == leave.total_leave_days(leaves, 'Hamburg')


def test_should_minus_half_day_if_ends_on_half_day():
    leaves = [
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

    assert 4 - 0.5 == leave.total_leave_days(leaves, 'Hamburg')


def test_should_minus_one_day_if_starts_and_ends_on_half_day():
    leaves = [
        {
            'type': 'Annual Leave',
            'period': {
                'startsOn': '28-05-2018',
                'startsOnHalf': True,
                'endsOn': '31-05-2018',
                'endsOnHalf': True
            }
        }
    ]

    assert 4 - 0.5 - 0.5 == leave.total_leave_days(leaves, 'Hamburg')


def test_should_minus_weekend_days_if_leave_period_include_weekends():
    leaves = [
        {
            'type': 'Annual Leave',
            'period': {
                'startsOn': '28-05-2018',
                'startsOnHalf': False,
                'endsOn': '04-06-2018',
                'endsOnHalf': False
            }
        }
    ]

    assert 8 - 2 == leave.total_leave_days(leaves, 'Hamburg')


def test_should_minus_public_holiday_days_if_leave_period_include_public_holiday():
    leaves = [
        {
            'type': 'Annual Leave',
            'period': {
                'startsOn': '30-04-2018',
                'startsOnHalf': False,
                'endsOn': '02-05-2018',
                'endsOnHalf': False
            }
        }
    ]

    assert 3 - 1 == leave.total_leave_days(leaves, 'Hamburg')


def test_should_calculate_multi_leaves():
    leaves = [
        {
            'type': 'Annual Leave',
            'period': {
                'startsOn': '30-04-2018',
                'startsOnHalf': False,
                'endsOn': '02-05-2018',
                'endsOnHalf': False
            }
        },
        {
            'type': 'Annual Leave',
            'period': {
                'startsOn': '28-05-2018',
                'startsOnHalf': False,
                'endsOn': '04-06-2018',
                'endsOnHalf': False
            }
        }
    ]

    assert 3 - 1 + 8 - 2 == leave.total_leave_days(leaves, 'Hamburg')


def test_should_calculate_leave_days_within_specified_year():
    leaves = [
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

    assert 1.0 + 1.0 == leave.total_leave_days(leaves, 'Hamburg', 2018)
