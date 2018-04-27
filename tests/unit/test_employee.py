from chatbot.actions import employee


def test_valid_user():
    assert True is employee._valid_user({'homeOffice': {'name': 'Berlin'}})
    assert True is employee._valid_user({'homeOffice': {'name': 'Hamburg'}})
    assert True is employee._valid_user({'homeOffice': {'name': 'Munich'}})
    assert True is employee._valid_user({'homeOffice': {'name': 'Cologne'}})

    assert False is employee._valid_user({'homeOffice': {'name': 'Barcelona'}})
    assert False is employee._valid_user({'homeOffice': {'name': 'Antarctica'}})
