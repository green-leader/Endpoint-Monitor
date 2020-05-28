'''Utilities to use within testing'''
from unittest import mock


def get_fake_get(status_code, content):
    '''Fake response for requests.get to use in mock patching takes in status_c\
ode and content'''
    m = mock.Mock()
    m.status_code = status_code
    m.content = content

    def fake_get(url):
        return m

    return fake_get
