import unittest
from click.testing import CliRunner
import testutils as utils
from unittest import mock

from monitor import cli
from monitor import core

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

    @mock.patch('requests.get', utils.get_fake_get(200, ''))
    def testAdd(self):
        runner = CliRunner()
        result = runner.invoke(cli.add, input='https://google.com\nTestInput')
        self.assertEqual(0, result.exit_code)

    @mock.patch('requests.get', utils.get_fake_get(200, ''))
    def testDelete(self):
        runner = CliRunner()
        runner.invoke(cli.add, input='https://google.com\nTestInput')
        result = runner.invoke(cli.delete, ['aHR0cHM6Ly9nb29nbGUuY29t'])
        self.assertEqual(0, result.exit_code)

    @mock.patch('requests.get', utils.get_fake_get(200, ''))
    def testBadDelete(self):
        runner = CliRunner()
        runner.invoke(cli.add, input='https://google.com\nTestInput')
        result = runner.invoke(cli.delete, ['BadDelete'])
        assert 'That doesnt appear to be a valid entry\n' == result.output
        self.assertEqual(1, result.exit_code)


if __name__ == '__main__':
    unittest.main()
