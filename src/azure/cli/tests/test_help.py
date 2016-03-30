from __future__ import print_function
import unittest
from six import StringIO

from azure.cli._logging import logger
from azure.cli.parser import AzCliCommandParser
from azure.cli.application import Application
import azure.cli._help_files
import logging
import mock
import sys
import azure.cli._util as util
from azure.cli._help import HelpAuthoringException

io = {}
def redirect_io(func):
    def wrapper(self):
        global io
        old_out = sys.stdout
        sys.stdout = io = StringIO()
        func(self)
        io.close()
        sys.stdout = old_out
    return wrapper

class Test_argparse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure initialization has occurred correctly
        import azure.cli.main
        logging.basicConfig(level=logging.DEBUG)

    @classmethod
    def tearDownClass(cls):
        logging.shutdown()

    @redirect_io
    def test_help_param(self):
        app = Application()
        def test_handler(args):
            pass

        cmd_table = {
            test_handler: {
                'name': 'n1',
                'arguments': [
                    {'name': '--arg -a', 'required': False},
                    {'name': '-b', 'required': False}
                    ]
                }
            }
        app.load_commands(cmd_table)

        cmd_result = app.execute('n1 -h'.split())
        self.assertIsNone(cmd_result)

        cmd_result = app.execute('n1 --help'.split())
        self.assertIsNone(cmd_result)

    @redirect_io
    def test_help_plain_short_description(self):
        app = Application()
        def test_handler(args):
            pass

        cmd_table = {
            test_handler: {
                'name': 'n1',
                'description': 'the description',
                'arguments': [
                    {'name': '--arg -a', 'required': False},
                    {'name': '-b', 'required': False}
                    ]
                }
            }
        app.load_commands(cmd_table)

        cmd_result = app.execute('n1 -h'.split())
        self.assertIsNone(cmd_result)
        self.assertEqual(True, 'n1: the description' in io.getvalue())

    @redirect_io
    def test_help_plain_long_description(self):
        app = Application()
        def test_handler(args):
            '''
            long description
            '''

        cmd_table = {
            test_handler: {
                'name': 'n1',
                'arguments': [
                    {'name': '--arg -a', 'required': False},
                    {'name': '-b', 'required': False}
                    ]
                }
            }
        app.load_commands(cmd_table)

        cmd_result = app.execute('n1 -h'.split())

        self.assertIsNone(cmd_result)
        self.assertEqual(True, io.getvalue().startswith('\nCommand\n    n1\n        long description'))

    @redirect_io
    def test_help_long_description_and_short_description(self):
        app = Application()
        def test_handler(args):
            '''
            long description
            '''

        cmd_table = {
            test_handler: {
                'name': 'n1',
                'description': 'short description',
                'arguments': [
                    {'name': '--arg -a', 'required': False},
                    {'name': '-b', 'required': False}
                    ]
                }
            }
        app.load_commands(cmd_table)

        cmd_result = app.execute('n1 -h'.split())
        self.assertIsNone(cmd_result)
        self.assertEqual(True, io.getvalue().startswith('\nCommand\n    n1: short description\n        long description'))

    @redirect_io
    def test_help_docstring_description_overrides_short_description(self):
        app = Application()
        def test_handler(args):
            '''
            short-summary: docstring summary
            '''

        cmd_table = {
            test_handler: {
                'name': 'n1',
                'description': 'short description',
                'arguments': [
                    {'name': '--arg -a', 'required': False},
                    {'name': '-b', 'required': False}
                    ]
                }
            }
        app.load_commands(cmd_table)

        cmd_result = app.execute('n1 -h'.split())
        self.assertIsNone(cmd_result)
        self.assertEqual(True, 'n1: docstring summary' in io.getvalue())

    @redirect_io
    def test_help_long_description_multi_line(self):
        app = Application()
        def test_handler(args):
            '''
            long-summary: |
                line1
                line2
            '''

        cmd_table = {
            test_handler: {
                'name': 'n1',
                'arguments': [
                    {'name': '--arg -a', 'required': False},
                    {'name': '-b', 'required': False}
                    ]
                }
            }
        app.load_commands(cmd_table)

        cmd_result = app.execute('n1 -h'.split())
        self.assertIsNone(cmd_result)

        self.assertEqual(True, io.getvalue().startswith('\nCommand\n    n1\n        line1\n        line2'))

    @redirect_io
    def test_help_params_documentations(self):
        app = Application()
        def test_handler(args):
            '''
            parameters: 
              - name: --foobar -fb
                type: string
                required: false
                short-summary: one line partial sentence
                long-summary: text, markdown, etc.
                populator-commands: 
                    - az vm list
                    - default
              - name: --foobar2 -fb2
                type: string
                required: true
                short-summary: one line partial sentence
                long-summary: paragraph(s)
            '''

        cmd_table = {
            test_handler: {
                'name': 'n1',
                'arguments': [
                    {'name': '--foobar -fb', 'required': False},
                    {'name': '--foobar2 -fb2', 'required': True},
                    {'name': '--foobar3 -fb3', 'required': False, 'help': 'the foobar3'}
                    ]
                }
            }
        app.load_commands(cmd_table)

        cmd_result = app.execute('n1 -h'.split())
        self.assertIsNone(cmd_result)
        s = '''
Command
    n1

Arguments
    --foobar -fb             : one line partial sentence
        text, markdown, etc.

        Values from: az vm list, default

    --foobar2 -fb2 [Required]: one line partial sentence
        paragraph(s)

    --foobar3 -fb3           : the foobar3

'''
        self.assertEqual(s, io.getvalue())

    @redirect_io
    def test_help_full_documentations(self):
        app = Application()
        def test_handler(args):
            '''
            short-summary: this module does xyz one-line or so
            long-summary: |
                this module.... kjsdflkj... klsfkj paragraph1
                this module.... kjsdflkj... klsfkj paragraph2
            parameters: 
              - name: --foobar -fb
                type: string
                required: false
                short-summary: one line partial sentence
                long-summary: text, markdown, etc.
                populator-commands: 
                    - az vm list
                    - default
              - name: --foobar2 -fb2
                type: string
                required: true
                short-summary: one line partial sentence
                long-summary: paragraph(s)
            examples:
              - name: foo example
                text: example details
            '''

        cmd_table = {
            test_handler: {
                'name': 'n1',
                'arguments': [
                    {'name': '--foobar -fb', 'required': False},
                    {'name': '--foobar2 -fb2', 'required': True}
                    ]
                }
            }
        app.load_commands(cmd_table)

        cmd_result = app.execute('n1 -h'.split())
        self.assertIsNone(cmd_result)
        s = '''
Command
    n1: this module does xyz one-line or so
        this module.... kjsdflkj... klsfkj paragraph1
        this module.... kjsdflkj... klsfkj paragraph2

Arguments
    --foobar -fb             : one line partial sentence
        text, markdown, etc.

        Values from: az vm list, default

    --foobar2 -fb2 [Required]: one line partial sentence
        paragraph(s)

Examples
    foo example
        example details
'''
        self.assertEqual(s, io.getvalue())

    @redirect_io
    def test_help_mismatched_required_params(self):
        app = Application()
        def test_handler(args):
            '''
            parameters: 
              - name: --foobar -fb
                type: string
                required: false
                short-summary: one line partial sentence
                long-summary: text, markdown, etc.
                populator-commands: 
                    - az vm list
                    - default
            '''

        cmd_table = {
            test_handler: {
                'name': 'n1',
                'arguments': [
                    {'name': '--foobar -fb', 'required': True}
                    ]
                }
            }
        app.load_commands(cmd_table)

        self.assertRaisesRegexp(HelpAuthoringException,
                               '.*mismatched required True vs\. False, --foobar -fb.*',
                                lambda: app.execute('n1 -h'.split()))

    @redirect_io
    def test_help_extra_help_params(self):
        app = Application()
        def test_handler(args):
            '''
            parameters: 
              - name: --foobar -fb
                type: string
                required: false
                short-summary: one line partial sentence
                long-summary: text, markdown, etc.
                populator-commands: 
                    - az vm list
                    - default
            '''

        cmd_table = {
            test_handler: {
                'name': 'n1',
                'arguments': [
                    {'name': '--foobar2 -fb2', 'required': True}
                    ]
                }
            }
        app.load_commands(cmd_table)

        self.assertRaisesRegexp(HelpAuthoringException,
                               '.*Extra help param --foobar -fb.*',
                                lambda: app.execute('n1 -h'.split()))

    @redirect_io
    def test_help_with_param_specified(self):
        app = Application()
        def test_handler(args):
            pass

        cmd_table = {
            test_handler: {
                'name': 'n1',
                'arguments': [
                    {'name': '--arg -a', 'required': False},
                    {'name': '-b', 'required': False}
                    ]
                }
            }
        app.load_commands(cmd_table)

        cmd_result = app.execute('n1 --arg -h'.split())
        self.assertIsNone(cmd_result)

        s = '''
Command
    n1

Arguments
    --arg -a

    -b

'''

        self.assertEqual(s, io.getvalue())

    @redirect_io
    def test_help_group_children(self):
        app = Application()
        def test_handler(args):
            pass

        cmd_table = {
            test_handler: {
                'name': 'group1 group2 n1',
                'arguments': [
                    {'name': '--foobar -fb', 'required': False},
                    {'name': '--foobar2 -fb2', 'required': True}
                    ]
                },
            test_handler: {
                'name': 'group1 group3 n1',
                'arguments': [
                    {'name': '--foobar -fb', 'required': False},
                    {'name': '--foobar2 -fb2', 'required': True}
                    ]
                }
            }
        app.load_commands(cmd_table)

        cmd_result = app.execute('group1'.split())
        self.assertIsNone(cmd_result)
        s = '\nSub-Commands:\n\n    group3\n'
        self.assertEqual(s, io.getvalue())

    @redirect_io
    def test_help_group_help(self):
        app = Application()
        def test_handler(args):
            '''
            short-summary: this module does xyz one-line or so
            long-summary: |
                this module.... kjsdflkj... klsfkj paragraph1
                this module.... kjsdflkj... klsfkj paragraph2
            parameters: 
              - name: --foobar -fb
                type: string
                required: false
                short-summary: one line partial sentence
                long-summary: text, markdown, etc.
                populator-commands: 
                    - az vm list
                    - default
              - name: --foobar2 -fb2
                type: string
                required: true
                short-summary: one line partial sentence
                long-summary: paragraph(s)
            examples:
              - name: foo example
                text: example details
            '''

        cmd_table = {
            test_handler: {
                'name': 'test_group1 test_group2 n1',
                'arguments': {}
                }
            }
        app.load_commands(cmd_table)

        cmd_result = app.execute('test_group1 test_group2 --help'.split())
        self.assertIsNone(cmd_result)
        s = '''
Group
    test_group1 test_group2: this module does xyz one-line or so
        this module.... kjsdflkj... klsfkj paragraph1
        this module.... kjsdflkj... klsfkj paragraph2

Sub-Commands
    n1

Examples
    foo example
        example details
'''
        self.assertEqual(s, io.getvalue())


if __name__ == '__main__':
    unittest.main()
