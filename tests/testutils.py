'''Utilities to use within testing'''
from unittest import mock
import base64

def get_fake_get(status_code, content):
    '''Fake response for requests.get to use in mock patching takes in status_c\
ode and content'''
    m = mock.Mock()
    m.status_code = status_code
    m.content = content

    def fake_get(url):
        return m

    return fake_get


def get_fake_listing():
    fake_listing = dict()
    pageEntry = dict()
    URL = base64.b64encode(b'https://example.com')
    pageEntry['URL'] = URL.decode()
    pageEntry['name'] = 'TestInput'
    pageEntry['hash'] = '1234'
    fake_listing[URL.decode()] = pageEntry
    return fake_listing
