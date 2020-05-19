import unittest
from unittest import mock
from monitor import core
import testutils as utils

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

    @mock.patch('requests.get', utils.get_fake_get(200, ''))
    def testAdd(self):
        u1 = dict()
        u1['Name'] = 'Google Homepage'
        u1['URL'] = 'aHR0cHM6Ly9nb29nbGUuY29t'
        u1['hash'] = ''
        core.add(u1)
        assert 1 == len(core.listing())

    @mock.patch('requests.get', utils.get_fake_get(200, ''))
    def testDeleteExisting(self):
        u1 = dict()
        u1['Name'] = 'Google Homepage'
        u1['URL'] = 'aHR0cHM6Ly9nb29nbGUuY29t'
        u1['hash'] = ''
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

    @mock.patch('requests.get', utils.get_fake_get(200, 'fake Request'))
    def testFetch(self):
        result = core.fetch(b'aHR0cDovL2Zha2VVUkw=')
        assert '8503b8403995daa720ccfe74bb9c8b167513ea5f' == result

    def get_fake_get_byte(status, content):
        m = mock.Mock()
        m.status_code = status
        m.content = bytes(content.encode('utf-8'))

        def fake_get(url):
            return m
        return fake_get

    @mock.patch('requests.get', get_fake_get_byte(200, 'fake Request'))
    def testFetchBytesData(self):
        result = core.fetch(b'aHR0cDovL2Zha2VVUkw=')
        assert '8503b8403995daa720ccfe74bb9c8b167513ea5f' == result


if __name__ == '__main__':
    unittest.main()
