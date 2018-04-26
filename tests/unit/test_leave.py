from chatbot.actions import leave


def test_valid_user():
    assert True is leave._valid_user({'homeOffice': {'name': 'Berlin'}})
    assert True is leave._valid_user({'homeOffice': {'name': 'Hamburg'}})
    assert True is leave._valid_user({'homeOffice': {'name': 'Munich'}})
    assert True is leave._valid_user({'homeOffice': {'name': 'Cologne'}})

    assert False is leave._valid_user({'homeOffice': {'name': 'Barcelona'}})
    assert False is leave._valid_user({'homeOffice': {'name': 'Antarctica'}})
