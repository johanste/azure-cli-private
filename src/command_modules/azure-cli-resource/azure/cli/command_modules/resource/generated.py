from azure.mgmt.resource.resources.operations.resource_groups_operations \
    import ResourceGroupsOperations
from azure.mgmt.resource.resources.operations.tags_operations import TagsOperations
from azure.mgmt.resource.resources.operations.deployments_operations import DeploymentsOperations
from azure.mgmt.resource.resources.operations.deployment_operations_operations \
    import DeploymentOperationsOperations
from azure.cli.commands._auto_command import build_operation, CommandDefinition
from azure.cli.commands import CommandTable, LongRunningOperation, patch_aliases
from azure.cli._locale import L

from ._params import PARAMETER_ALIASES, _resource_client_factory
from .custom import ConvenienceResourceGroupCommands, ConvenienceResourceCommands

command_table = CommandTable()

build_operation(
    'resource group', 'resource_groups', _resource_client_factory,
    [
        CommandDefinition(
            ResourceGroupsOperations.delete,
            LongRunningOperation(L('Deleting resource group'), L('Resource group deleted')),
            id_parameters=['resource_group_name']),
        CommandDefinition(ResourceGroupsOperations.get, 'ResourceGroup', 'show',
                              id_parameters=['resource_group_name']),
        CommandDefinition(ResourceGroupsOperations.check_existence, 'Bool', 'exists',
                              id_parameters=['resource_group_name']),
    ],
    command_table, PARAMETER_ALIASES)

build_operation(
    'resource group', None, ConvenienceResourceGroupCommands,
    [
        CommandDefinition(ConvenienceResourceGroupCommands.list, '[ResourceGroup]'),
        CommandDefinition(ConvenienceResourceGroupCommands.create, 'ResourceGroup',
                              id_parameters=['resource_group_name']),
    ],
    command_table, PARAMETER_ALIASES)

build_operation(
    'resource', None, ConvenienceResourceCommands,
    [
        CommandDefinition(ConvenienceResourceCommands.list, '[Resource]'),
        CommandDefinition(ConvenienceResourceCommands.show, 'Resource', 
                              id_parameters=('resource_group_name', 'resource_name')),
    ],
    command_table, PARAMETER_ALIASES)

build_operation(
    'tag', 'tags', _resource_client_factory,
    [
        CommandDefinition(TagsOperations.list, '[Tag]'),
        CommandDefinition(TagsOperations.create_or_update, 'Tag', 'create'),
        CommandDefinition(TagsOperations.delete, None, 'delete'),
        CommandDefinition(TagsOperations.create_or_update_value, 'Tag', 'add-value'),
        CommandDefinition(TagsOperations.delete_value, None, 'remove-value'),
    ],
    command_table, patch_aliases(PARAMETER_ALIASES, {
        'tag_name': {'name': '--name -n'},
        'tag_value': {'name': '--value'}
    }))

build_operation(
    'resource group deployment', 'deployments', _resource_client_factory,
    [
        CommandDefinition(DeploymentsOperations.list, '[Deployment]', id_parameters=['resource_group_name']),
        CommandDefinition(DeploymentsOperations.get, 'Deployment', 'show', id_parameters=('resource_group_name', 'deployment_name')),
        #CommandDefinition(DeploymentsOperations.validate, 'Object'),
        #CommandDefinition(DeploymentsOperations.delete, 'Object'),
        CommandDefinition(DeploymentsOperations.check_existence, 'Bool', 'exists', id_parameters=('resource_group_name', 'deployment_name')),
        #CommandDefinition(DeploymentsOperations.cancel, 'Object'),
        #CommandDefinition(DeploymentsOperations.create_or_update, 'Object', 'create'),
    ],
    command_table)

build_operation(
    'resource group deployment operation', 'deployment_operations', _resource_client_factory,
    [
        CommandDefinition(DeploymentOperationsOperations.list, '[DeploymentOperations]', id_parameters=('resource_group_name', 'deployment_name')),
        CommandDefinition(DeploymentOperationsOperations.get, 'DeploymentOperations', 'show', id_parameters=('resource_group_name', 'deployment_name', 'operation_id'))
    ],
    command_table)
