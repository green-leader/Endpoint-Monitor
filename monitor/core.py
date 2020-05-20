# Monitor Core
import shelve
import dbm
import base64
import requests
import hashlib


class NoDB(Exception):
    pass


class BadURL(Exception):
    pass


class EmptyListError(Exception):
    pass


shelfFile = 'pageListing.dat'


def add(data):
    '''Fetch has, then add data to data store'''
    data['hash'] = fetch(data['URL'])
    with shelve.open(shelfFile, 'c') as shelf:
        shelf[data['URL']] = data


def listing():
    '''Get all data in data store as dictionary'''
    try:
        with shelve.open(shelfFile, 'r') as shelf:
            return dict(shelf)
    except dbm.error:
        return dict()


def delete(delURL):
    with shelve.open(shelfFile, 'w') as shelf:
        try:
            del shelf[delURL]
        except dbm.error:
            raise NoDB('There is not a database to delete from')


def update(checkURL=''):
    '''check if item(s) have changed'''
    if checkURL == '' or checkURL is None:  # assume request for all
        records = listing()
        if len(records) == 0:
            raise EmptyListError('There\'s nothing to check, database empty')
    pass


def fetch(URL):
    '''fetch base64 Encoded URL returning hexdigest of content'''
    urlDecoded = base64.b64decode(URL)
    if urlDecoded[0:4] != b'http':
        raise BadURL('Invalid URL protocol')
    page = requests.get(urlDecoded)
    response = hashlib.sha1()
    try:
        page.content = page.content.encode('utf-8')
    except AttributeError:
        pass

    response.update(page.content)
    return response.hexdigest()
