import argparse
import re
from collections import defaultdict
from azure.cli.commands.client_factory import get_mgmt_service_client
from azure.mgmt.resource.resources import ResourceManagementClient
from azure.cli.application import APPLICATION
from azure.cli._util import CLIError

regex = re.compile('/subscriptions/(?P<subscription>[^/]*)/resourceGroups/(?P<resource_group>[^/]*)'
                   '/providers/(?P<namespace>[^/]*)/(?P<type>[^/]*)/(?P<name>[^/]*)'
                   '(/(?P<child_type>[^/]*)/(?P<child_name>[^/]*))?')

def resource_id(**kwargs):
    '''Create a valid resource id string from the given parts

    The method accepts the following keyword arguments:

        - subscription      Subscription id
        - resource_group    Name of resource group
        - namespace         Namespace for the resource provider (i.e. Microsoft.Compute)
        - type              Type of the resource (i.e. virtualMachines)
        - name              Name of the resource (or parent if child_name is also specified)
        - child_type        Type of the child resource
        - child_name        Name of the child resource
    '''
    rid = '/subscriptions/{subscription}'.format(**kwargs)
    try:
        rid = '/'.join((rid, 'resourceGroups/{resource_group}'.format(**kwargs)))
        rid = '/'.join((rid, 'providers/{namespace}'.format(**kwargs)))
        rid = '/'.join((rid, '{type}/{name}'.format(**kwargs)))
        rid = '/'.join((rid, '{child_type}/{child_name}'.format(**kwargs)))
    except KeyError:
        pass
    return rid

def parse_resource_id(rid):
    '''Build a dictionary with the following key/value pairs (if found)

        - subscription      Subscription id
        - resource_group    Name of resource group
        - namespace         Namespace for the resource provider (i.e. Microsoft.Compute)
        - type              Type of the resource (i.e. virtualMachines)
        - name              Name of the resource (or parent if child_name is also specified)
        - child_type        Type of the child resource
        - child_name        Name of the child resource
    '''
    m = regex.match(rid)
    if m:
        result = m.groupdict()
    else:
        result = dict(name=rid)

    return {key:value for key, value in result.items() if value is not None}

def is_valid_resource_id(rid, exception_type=None):
    is_valid = False
    try:
        is_valid = rid and resource_id(**parse_resource_id(rid)) == rid
    except KeyError:
        pass
    if not is_valid and exception_type:
        raise exception_type()
    return is_valid

class ResourceId(str):

    def __new__(cls, val):
        if not is_valid_resource_id(val):
            raise ValueError()
        return str.__new__(cls, val)

def resource_exists(resource_group, name, namespace, type, **_): # pylint: disable=redefined-builtin
    '''Checks if the given resource exists.
    '''
    odata_filter = "resourceGroup eq '{}' and name eq '{}'" \
        " and resourceType eq '{}/{}'".format(resource_group, name, namespace, type)
    client = get_mgmt_service_client(ResourceManagementClient).resources
    existing = len(list(client.list(filter=odata_filter))) == 1
    return existing

def add_id_parameters(command_table):

    def split_action(arguments):
        class SplitAction(argparse.Action): #pylint: disable=too-few-public-methods

            def __call__(self, parser, namespace, values, option_string=None):
                try:
                    parts = parse_resource_id(values)
                    for arg in [arg for arg in arguments.values() if arg.id_part]:
                        setattr(namespace, arg.name, parts[arg.id_part])
                except Exception as ex:
                    raise ValueError(ex)

        return SplitAction

    def command_loaded_handler(command):
        if not 'name' in [arg.id_part for arg in command.arguments.values() if arg.id_part]:
            # Only commands with a resource name are candidates for an id parameter
            return
        if command.name.split()[-1] == 'create':
            # Somewhat blunt hammer, but any create commands will not have an automatic id
            # parameter
            return

        required_arguments = []
        optional_arguments = []
        for arg in [argument for argument in command.arguments.values() if argument.id_part]:
            if arg.options.get('required', False):
                required_arguments.append(arg)
            else:
                optional_arguments.append(arg)
            arg.required = False

        def required_values_validator(namespace):
            errors = [arg for arg in required_arguments
                      if getattr(namespace, arg.name, None) is None]

            if errors:
                missing_required = ' '.join((arg.options_list[0] for arg in errors))
                raise CLIError('({} | {}) are required'.format(missing_required, '--id'))

        command.add_argument(argparse.SUPPRESS,
                             '--id',
                             metavar='RESOURCE_ID',
                             help='ID of resource',
                             action=split_action(command.arguments),
                             type=ResourceId,
                             validator=required_values_validator)

    for command in command_table.values():
        command_loaded_handler(command)

    APPLICATION.remove(APPLICATION.COMMAND_TABLE_LOADED, add_id_parameters)

APPLICATION.register(APPLICATION.COMMAND_TABLE_LOADED, add_id_parameters)

def _get_name_path(path):
    pathlist = path.split('.')

    return pathlist.pop(), pathlist

def _find_property(instance, path):
    for part in path:
        if isinstance(instance, dict):
            instance = instance[part]
        else:
            instance = getattr(instance, part)
    return instance

def set_properties(instance, expression):
    key, value = expression.split('=', 1)
    name, path = _get_name_path(key)
    instance = _find_property(instance, path)
    if isinstance(instance, dict):
        instance[name] = value
    else:
        setattr(instance, name, value)

def add_properties(instance, argument_values):
    # The first argument indicates the path to the collection
    # to add to. 
    list_attribute_path = argument_values.pop(0).split('.')

    # Find the actual list to add the new object to
    list_to_add_to = _find_property(instance, list_attribute_path) # TODO: Create list if it doesn't exist

    new_value = defaultdict(lambda: {})
    for expression in argument_values:
        set_properties(new_value, expression)
    list_to_add_to.append(new_value)

def remove_properties(instance, argument_values):
    # The first argument indicates the path to the collection
    # to add to. 
    list_attribute_path = argument_values.pop(0).split('.')
    list_index = argument_values.pop(0)

    # Find the actual list to add the new object to
    list_to_remove_from = _find_property(instance, list_attribute_path) # TODO: Create list if it doesn't exist
    list_to_remove_from.pop(int(list_index))

def register_generic_update(name, getter, setter, setter_arg_name='parameters'):
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.cli.commands import CliCommand, command_table
    from azure.cli.commands._introspection import extract_args_from_signature

    get_arguments = dict(extract_args_from_signature(getter))
    set_arguments = dict(extract_args_from_signature(setter))

    def handler(args):
        getterargs= {key: val for key, val in args.items()
                     if key in get_arguments}
        instance = getter(**getterargs)

        # Make modifications...
        for remove_expression in args['properties_to_remove']:
            remove_properties(instance, remove_expression)

        for set_expression in args['properties_to_set']:
            set_properties(instance, set_expression)

        for add_expression in args['properties_to_add']:
            add_properties(instance, add_expression)

        # Done... update the instance!
        getterargs[setter_arg_name] = instance
        opres = setter(**getterargs)
        return opres.result() if isinstance(opres, AzureOperationPoller) else result

    cmd = CliCommand(name, handler)
    cmd.arguments.update(set_arguments)
    cmd.arguments.update(get_arguments)
    cmd.arguments.pop(setter_arg_name, None)
    cmd.add_argument('properties_to_set', '--set', nargs='+', default=[])
    cmd.add_argument('properties_to_add', '--add', nargs='+', action='append', default=[])
    cmd.add_argument('properties_to_remove', '--remove', nargs='+', action='append', default=[])
    command_table[name] = cmd
