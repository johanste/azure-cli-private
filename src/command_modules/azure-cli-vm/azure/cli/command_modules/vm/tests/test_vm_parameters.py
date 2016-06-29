﻿import unittest

from azure.cli.application import APPLICATION, Configuration
from azure.cli._util import CLIError

def mock_echo_args(command_name, parameters):
    try:
        argv = ' '.join((command_name, parameters)).split()
        APPLICATION.initialize(Configuration(argv))
        command_table = APPLICATION.configuration.get_command_table()
        prefunc = command_table[command_name].handler
        command_table[command_name].handler = lambda args: args
        parsed_namespace = APPLICATION.execute(argv)
        return parsed_namespace
    finally:
        command_table[command_name].handler = prefunc

class Test_ArgumentParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_parse_vm_show(self):

        # Flag can be passed before positional name
        args = mock_echo_args('vm show', '-g funky dory')
        self.assertDictEqual({
            'api_version': '2016-03-30',
            'expand': None,
            'resource_group_name': 'funky',
            'vm_name': 'dory'
            }, args)

        # Flag can be passed after positional name
        args = mock_echo_args('vm show', 'dory --resource-group funky')
        self.assertDictEqual({
            'api_version': '2016-03-30',
            'expand': None,
            'resource_group_name': 'funky',
            'vm_name': 'dory'
            }, args)

        # If we use an ID as the positional parameter, we should
        # extract the resource group and name from it...
        args = mock_echo_args('vm show', '/subscriptions/00000000-0000-0000-0000-0123456789abc/resourceGroups/thisisaresourcegroup/providers/Microsoft.Compute/virtualMachines/thisisavmname')
        self.assertDictEqual({
            'api_version': '2016-03-30',
            'expand': None,
            'resource_group_name': 'thisisaresourcegroup',
            'vm_name': 'thisisavmname'
            }, args)

        # Invalid resource ID should trigger the missing resource group
        # parameter failure
        with self.assertRaises(CLIError):
            mock_echo_args('vm show', '/broken')

        # Got to provide a resource group if you are using a simple name and
        # not an ID as a parameter
        with self.assertRaises(CLIError):
            mock_echo_args('vm show', 'missing-resource-group')

    def test_parse_vm_list(self):
        # Resource group name is optional for vm list, so
        # we should see a successfully parsed namespace
        args = mock_echo_args('vm list', '')
        self.assertDictEqual({
            'resource_group_name': None,
            }, args)

        # if resource group name is specified, however, 
        # it should get passed through...
        args = mock_echo_args('vm list', '-g hullo')
        self.assertDictEqual({
            'resource_group_name': 'hullo',
            }, args)

if __name__ == '__main__':
    unittest.main()
