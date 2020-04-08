import unittest
from click.testing import CliRunner
from Monitor import cli
from Monitor import core

import tempfile
import os


class CliTest(unittest.TestCase):
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

    def testList(self):
        runner = CliRunner()
        result = runner.invoke(cli.listing)
        self.assertEqual(0, result.exit_code)
        self.assertEqual('', result.output)

    def testAdd(self):
        runner = CliRunner()
        result = runner.invoke(cli.add, input='https://google.com\nTestInput')
        print(result.output)
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
