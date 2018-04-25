def pytest_addoption(parser):
    parser.addoption('--e2e', action='store_true', dest="e2e",
                     default=False, help="enable end to end tests")


def pytest_configure(config):
    if not config.option.e2e:
        setattr(config.option, 'markexpr', 'not e2e')
