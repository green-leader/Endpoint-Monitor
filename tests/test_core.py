import unittest
from Monitor import core

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
        u1 = ['https://www.google.com/', 123]
        core.add(u1)
        assert 1 == len(core.listing())

    def testDeleteExisting(self):
        u1 = ['https://www.google.com/', 123]
        core.add(u1)
        core.delete(u1[0])
        self.assertEqual(0, len(core.listing()))

    def testDeleteNotExisting(self):
        u1 = ['https://www.google.com/', 123]
        with self.assertRaises(dbm.error):
            core.delete(u1[0])


if __name__ == '__main__':
    unittest.main()
