from __future__ import print_function
from ..commands import CommandTable
from .._locale import L

command_table = CommandTable()

def get_command_table(): # pylint:disable=duplicate-code
    return command_table

@command_table.command('taskhelp deploy-arm-template',
                       description=L('How to deploy and ARM template using Azure CLI.'))
def deploy_template_help(args): #pylint: disable=unused-argument
    print(L("""
***********************
ARM Template Deployment
***********************

Could this be helpful?  Let us know!
====================================

1. First Step
2. Second Step

And you're done!
"""))
