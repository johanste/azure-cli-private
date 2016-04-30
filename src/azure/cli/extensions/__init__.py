import argparse
from .query import register as register_query
from .transform import register as register_transform

class IdAction(argparse.Action):

    def __init__(self, **kwargs):
        self.name_dest = kwargs.pop('name_dest')
        super(IdAction, self).__init__(**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        parts = values.split('/')
        if len(parts) > 7 and parts[3] == 'resourceGroups':
            setattr(namespace, self.name_dest, parts[8])
            setattr(namespace, 'resource_group_name', parts[4])
            rgaction = parser.super_actions[('--resource-group', '-g')]
            rgaction.required = False
            rnaction = parser.super_actions[('--name', '-n')]
            rnaction.required = False
        else:
            raise argparse.ArgumentError(self, 'Broken id, dude!')

def register_id_adder(application):
    def adder(command_table):
        for command in command_table:
            options = {option['_semantic_type']: option
                       for option in command['arguments']
                       if option.get('_semantic_type', None)
                       in ('resource_group_name', 'resource_name')}
            if len(options) == 2:
                command['arguments'].append({
                    'name': '--id',
                    'name_dest': options['resource_name']['dest'],
                    'metavar': 'ID',
                    'action': IdAction,
                    'required': False,
                    })

    application.register(application.COMMAND_TABLE_LOADED, adder)

def register_extensions(application):
    register_query(application)
    register_transform(application)
    register_id_adder(application)
