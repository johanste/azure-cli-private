﻿# pylint: disable=line-too-long
from azure.mgmt.resource.resources.operations.resources_operations import ResourcesOperations
from azure.mgmt.resource.resources.operations.providers_operations import ProvidersOperations
from azure.mgmt.resource.resources.operations.resource_groups_operations \
    import ResourceGroupsOperations
from azure.mgmt.resource.resources.operations.tags_operations import TagsOperations
from azure.mgmt.resource.resources.operations.deployments_operations import DeploymentsOperations
from azure.mgmt.resource.resources.operations.deployment_operations_operations \
    import DeploymentOperationsOperations

from azure.cli.commands import cli_command
from azure.cli.command_modules.resource._factory import _resource_client_factory
from azure.cli.command_modules.resource.custom import (
    list_resource_groups, create_resource_group, export_group_as_template,
    list_resources, move_resource,
    deploy_arm_template, validate_arm_template, tag_resource, export_deployment_as_template,
    register_provider, unregister_provider
)

# Resource group commands
factory = lambda _: _resource_client_factory().resource_groups
cli_command('resource group delete', ResourceGroupsOperations.delete, factory)
cli_command('resource group show', ResourceGroupsOperations.get, factory)
cli_command('resource group exists', ResourceGroupsOperations.check_existence, factory)
cli_command('resource group list', list_resource_groups)
cli_command('resource group create', create_resource_group)
cli_command('resource group export', export_group_as_template)

# Resource commands
factory = lambda _: _resource_client_factory().resources
cli_command('resource exists', ResourcesOperations.check_existence, factory)
cli_command('resource delete', ResourcesOperations.delete, factory)
cli_command('resource show', ResourcesOperations.get, factory)
cli_command('resource list', list_resources)
cli_command('resource tag', tag_resource)
cli_command('resource move', move_resource)

# Resource provider commands
factory = lambda _: _resource_client_factory().providers
cli_command('resource provider list', ProvidersOperations.list, factory)
cli_command('resource provider show', ProvidersOperations.get, factory)
cli_command('resource provider register', register_provider)
cli_command('resource provider unregister', unregister_provider)

# Tag commands
factory = lambda _: _resource_client_factory().tags
cli_command('tag list', TagsOperations.list, factory)
cli_command('tag create', TagsOperations.create_or_update, factory)
cli_command('tag delete', TagsOperations.delete, factory)
cli_command('tag add-value', TagsOperations.create_or_update_value, factory)
cli_command('tag remove-value', TagsOperations.delete_value, factory)

# Resource group deployment commands
factory = lambda _: _resource_client_factory().deployments
cli_command('resource group deployment create', deploy_arm_template)
cli_command('resource group deployment list', DeploymentsOperations.list, factory)
cli_command('resource group deployment show', DeploymentsOperations.get, factory)
cli_command('resource group deployment validate', validate_arm_template)
cli_command('resource group deployment exists', DeploymentsOperations.check_existence, factory)
cli_command('resource group deployment export', export_deployment_as_template)

# Resource group deployment operations commands
factory = lambda _: _resource_client_factory().deployment_operations
cli_command('resource group deployment operation list', DeploymentOperationsOperations.list, factory)
cli_command('resource group deployment operation show', DeploymentOperationsOperations.get, factory)
