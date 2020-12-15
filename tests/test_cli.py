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

    def testListEmpty(self):
        core.listing()
        runner = CliRunner()
        result = runner.invoke(cli.listing)
        self.assertEqual(0, result.exit_code)
        self.assertEqual('', result.output)

    @mock.patch('monitor.core.listing', utils.get_fake_listing)
    def testListOneItems(self):
        runner = CliRunner()
        result = runner.invoke(cli.listing)
        self.assertEqual(0, result.exit_code)
        expectedOutput = "aHR0cHM6Ly9leGFtcGxlLmNvbQ==: {'URL': 'aHR0cHM6Ly9leGFtcGxlLmNvbQ==', 'name': 'TestInput', 'hash': '1234'}\n"
        self.assertEqual(expectedOutput, result.output)

    def testCheckEmpty(self):
        runner = CliRunner()
        result = runner.invoke(cli.check)
        self.assertEqual(1, result.exit_code)

    @mock.patch('monitor.core.listing', utils.get_fake_listing)
    @mock.patch('requests.get', utils.get_fake_get(200, '1234'))
    def testCheckOneItemNochange(self):
        runner = CliRunner()
        result = runner.invoke(cli.check)
        self.assertEqual(0, result.exit_code)

    @mock.patch('monitor.core.listing', utils.get_fake_listing)
    @mock.patch('requests.get', utils.get_fake_get(200, '2345'))
    def testCheckOneItemchange(self):
        runner = CliRunner()
        result = runner.invoke(cli.check)
        self.assertEqual(0, result.exit_code)

    @mock.patch('requests.get', utils.get_fake_get(200, ''))
    def testAdd(self):
        runner = CliRunner()
        result = runner.invoke(cli.add, input='https://google.com\nTestInput')
        self.assertEqual(0, result.exit_code)

    def testAddBadURL(self):
        runner = CliRunner()
        result = runner.invoke(cli.add, input='example.com\nTestInput')
        self.assertEqual(1, result.exit_code)

    def testAddError(self):
        runner = CliRunner()
        result = runner.invoke(cli.add, input='http://\nTestInput')
        self.assertEqual(1, result.exit_code)

    @mock.patch('requests.get', utils.get_fake_get(200, ''))
    def testDelete(self):
        runner = CliRunner()
        runner.invoke(cli.add, input='https://google.com\nTestInput')
        result = runner.invoke(cli.delete, ['aHR0cHM6Ly9nb29nbGUuY29t'])
        self.assertEqual(0, result.exit_code)

    @mock.patch('requests.get', utils.get_fake_get(200, ''))
    def testDeleteNoInput(self):
        runner = CliRunner()
        runner.invoke(cli.add, input='https://example.com\nTestInput')
        result = runner.invoke(cli.delete)
        self.assertEqual(1, result.exit_code)

    @mock.patch('requests.get', utils.get_fake_get(200, ''))
    def testDeleteError(self):
        runner = CliRunner()
        result = runner.invoke(cli.delete)
        self.assertEqual(1, result.exit_code)

    @mock.patch('requests.get', utils.get_fake_get(200, ''))
    def testBadDelete(self):
        runner = CliRunner()
        runner.invoke(cli.add, input='https://google.com\nTestInput')
        result = runner.invoke(cli.delete, ['BadDelete'])
        assert 'That doesnt appear to be a valid entry\n' == result.output
        self.assertEqual(1, result.exit_code)


if __name__ == '__main__':
    unittest.main()
