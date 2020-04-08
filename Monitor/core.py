# Monitor Core
import shelve
import dbm


class NoDB(Exception):
    pass


shelfFile = 'pageListing.dat'


def add(data):
    '''Add data to data store'''
    with shelve.open(shelfFile, 'c') as shelf:
        shelf[data['URL']] = data


def listing():
    '''Get all data in data store as dictionary'''
    with shelve.open(shelfFile, 'r') as shelf:
        return dict(shelf)


def delete(delURL):
    with shelve.open(shelfFile, 'w') as shelf:
        try:
            del shelf[delURL]
        except dbm.error:
            raise NoDB('There is not a database to delete from')


def update():
    pass
