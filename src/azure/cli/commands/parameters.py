import argparse
import time
import random

# pylint: disable=line-too-long
from azure.cli.commands import CliArgumentType, register_cli_argument
from azure.cli.commands.validators import validate_tag, validate_tags
from azure.cli._util import CLIError
from azure.cli.commands.client_factory import (get_subscription_service_client,
                                               get_mgmt_service_client)
from azure.mgmt.resource.subscriptions import SubscriptionClient

from azure.mgmt.resource.resources import ResourceManagementClient

def get_subscription_locations():
    subscription_client, subscription_id = get_subscription_service_client(SubscriptionClient)
    return list(subscription_client.subscriptions.list_locations(subscription_id))

def get_location_completion_list(prefix, **kwargs):#pylint: disable=unused-argument
    result = get_subscription_locations()
    return [l.name for l in result]

def get_one_of_subscription_locations():
    result = get_subscription_locations()
    if result:
        return next((r.name for r in result if r.name.lower() == 'westus'), result[0].name)
    else:
        raise CLIError('Current subscription does not have valid location list')

def get_resource_groups():
    rcf = get_mgmt_service_client(ResourceManagementClient)
    return list(rcf.resource_groups.list())

def get_resource_group_completion_list(prefix, **kwargs):#pylint: disable=unused-argument
    result = get_resource_groups()
    return [l.name for l in result]

def get_resources_in_resource_group(resource_group_name, resource_type=None):
    rcf = get_mgmt_service_client(ResourceManagementClient)
    filter_str = "resourceType eq '{}'".format(resource_type) if resource_type else None
    return list(rcf.resource_groups.list_resources(resource_group_name, filter=filter_str))

def get_resources_in_subscription(resource_type=None):
    rcf = get_mgmt_service_client(ResourceManagementClient)
    filter_str = "resourceType eq '{}'".format(resource_type) if resource_type else None
    return list(rcf.resources.list(filter=filter_str))

def get_resource_name_completion_list(resource_type=None):
    def completer(prefix, action, parsed_args, **kwargs):#pylint: disable=unused-argument
        if parsed_args.resource_group_name:
            rg = parsed_args.resource_group_name
            return [r.name for r in get_resources_in_resource_group(rg, resource_type=resource_type)]
        else:
            return [r.name for r in get_resources_in_subscription(resource_type=resource_type)]
    return completer

def _split_id(id_string):
    parts = id_string.split('/')[1:]
    return parts

def _is_id(parts):
    return len(parts) > 7 and parts[0] == 'subscriptions' and parts[2] == 'resourceGroups' and parts[4] == 'providers'

def splitter(resource_name_dest, rg_name_dest='resource_group_name', child_resource_name_dest=None):
    def func(namespace):
        parts = _split_id(getattr(namespace, resource_name_dest, ''))
        if _is_id(parts):
            setattr(namespace, resource_name_dest, parts[7])
            setattr(namespace, rg_name_dest, parts[3])
            if child_resource_name_dest:
                setattr(namespace, child_resource_name_dest, parts[9])
        else:
            if getattr(namespace, rg_name_dest) is None:
                raise argparse.ArgumentError(None, 'Missing resource group name')
            if child_resource_name_dest and not getattr(namespace, child_resource_name_dest):
                raise argparse.ArgumentError(None, 'Missing child resource name')
    return func

resource_group_name_type = CliArgumentType(
    options_list=('--resource-group', '-g'),
    completer=get_resource_group_completion_list,
    help='Name of resource group')

name_type = CliArgumentType(options_list=(), help='the primary resource name', metavar='(RESOURCEID | NAME -g RESOURCEGROUP)', required=CliArgumentType.REMOVE)
new_name_type = CliArgumentType(options_list=('--name', '-n'), metavar='NAME', required=True, validator=None)

location_type = CliArgumentType(
    options_list=('--location', '-l'),
    completer=get_location_completion_list,
    help='Location.', metavar='LOCATION')

tags_type = CliArgumentType(
    type=validate_tags,
    help='multiple semicolon separated tags in \'key[=value]\' format. Omit value to clear tags.',
    nargs='?',
    const=''
)

tag_type = CliArgumentType(
    type=validate_tag,
    help='a single tag in \'key[=value]\' format. Omit value to clear tags.',
    nargs='?',
    const=''
)

register_cli_argument('', 'resource_group_name', resource_group_name_type)
register_cli_argument('', 'location', location_type)
register_cli_argument('', 'deployment_name',
                      CliArgumentType(help=argparse.SUPPRESS, required=False,
                                      default='azurecli' + str(time.time())
                                      + str(random.randint(1, 100000))))
