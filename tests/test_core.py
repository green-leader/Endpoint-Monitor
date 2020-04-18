import unittest
from monitor import core

import os
import tempfile
import dbm


class CoreTest(unittest.TestCase):
    def setUp(self):
        fd, self.tempShelf = tempfile.mkstemp(suffix='.dat')
        os.close(fd)
        core.shelfFile = self.tempShelf
        if os.path.exists(self.tempShelf):
            os.remove(self.tempShelf)
        pass

    def tearDown(self):
        if os.path.exists(self.tempShelf):
            os.remove(self.tempShelf)
        pass

    def testAdd(self):
        u1 = dict()
        u1['Name'] = 'Google Homepage'
        u1['URL'] = 'aHR0cHM6Ly9nb29nbGUuY29t'
        u1['hash'] = 'sha1:1234'
        core.add(u1)
        assert 1 == len(core.listing())

    def testDeleteExisting(self):
        u1 = dict()
        u1['Name'] = 'Google Homepage'
        u1['URL'] = 'aHR0cHM6Ly9nb29nbGUuY29t'
        u1['hash'] = 'sha1:1234'
        core.add(u1)
        core.delete(u1['URL'])
        self.assertEqual(0, len(core.listing()))

    def testDeleteNotExisting(self):
        u1 = ['https://www.google.com/', 123]
        with self.assertRaises(dbm.error):
            core.delete(u1[0])

    def testFetchBadProtocol(self):
        '''Test fetch with unsupported protocol'''
        with self.assertRaises(core.BadURL):
            core.fetch(b'YmFkcHJvdG9jb2w=').decode()

    def testFetch(self):
        assert '4a3ce8ee11e091dd7923f4d8c6e5b5e41ec7c047' \
          == core.fetch(b'aHR0cDovL2V4YW1wbGUuY29t')


if __name__ == '__main__':
    unittest.main()
