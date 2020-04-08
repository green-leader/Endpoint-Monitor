import unittest
from click.testing import CliRunner
from Monitor import cli


class CliTest(unittest.TestCase):
    def testList(self):
        runner = CliRunner()
        result = runner.invoke(cli.listing)
        self.assertEqual(0, result.exit_code)
        self.assertEqual('', result.output)


if __name__ == '__main__':
    unittest.main()
