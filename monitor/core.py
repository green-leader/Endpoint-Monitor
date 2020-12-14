# Monitor Core
import shelve
import dbm
import base64
import requests
import hashlib
import bs4


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
    _updateEntry(data)


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


def _updateEntry(data):
    with shelve.open(shelfFile, 'c') as shelf:
        shelf[data['URL']] = data


def update(checkURL=''):
    '''check if item(s) have changed'''
    updatedRecords = list()
    records = listing()
    if len(records) == 0:
        raise EmptyListError('There\'s nothing to check, database empty')
    if checkURL == '' or checkURL is None:  # assume request for all
        for record in records:
            response = fetch(record)
            if records[record]['hash'] != response:
                records[record]['hash'] = response
                _updateEntry(records[record])
                updatedRecords.append(record)
    else:
        response = fetch(checkURL)
        if records[checkURL]['hash'] != response:
            records[checkURL]['hash'] = response
            _updateEntry(records[checkURL])
            updatedRecords.append(checkURL)
    return updatedRecords


def fetch(URL):
    '''fetch base64 Encoded URL returning hexdigest of content'''
    urlDecoded = base64.b64decode(URL)
    if urlDecoded[0:4] != b'http':
        raise BadURL('Invalid URL protocol')
    page = requests.get(urlDecoded)
    page.raise_for_status()

    response = hashlib.sha1()

    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    for tag in soup(['script', 'style']):
        tag.extract()

    response.update(soup.encode('utf-8'))
    return response.hexdigest()
