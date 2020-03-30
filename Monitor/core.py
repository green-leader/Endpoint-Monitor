# Monitor Core
import shelve
import sys

shelfFile = 'pageListing.dat'


def add(data):
    '''Add data to data store'''
    with shelve.open(shelfFile, 'c') as shelf:
        shelf[data[0]] = data


def listing():
    '''Get all data in data store as dictionary'''
    with shelve.open(shelfFile, 'r') as shelf:
        return dict(shelf)


def update():
    pass


def delete():
    pass
