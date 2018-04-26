from chatbot.actions import taken_leaves


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

    assert 1 + 2 == taken_leaves.get_leaves_taken({'employeeId': '42', 'homeOffice': {'name': 'Berlin'}}, 2018)


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

    assert 2 + 3 == taken_leaves.get_leaves_taken({'employeeId': '42', 'homeOffice': {'name': 'Berlin'}}, 2018)
