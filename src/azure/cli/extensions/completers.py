def register(application):
    application.register(application.COMMAND_TABLE_LOADED, _annotate_command_table)

def _annotate_command_table(command_table):
    for _, command_metadata in command_table.iteritems():
        for option in command_metadata['arguments']:
            # TODO: dest is not the best key. Suggestion is to provide semantic type information
            if option.get('dest') == 'account_name':
                option['completer'] = option.get('completer', _storage_account_name_completer)
            elif option.get('dest') == 'resource_group_name':
                option['completer'] = option.get('completer', _resource_group_completer)

def _resource_group_completer(**kwargs):
    from ..commands.resource import list_groups

    for group in list_groups({}):
        yield group.name

def _storage_account_name_completer(**kwargs):
    from ..commands.storage import list_accounts

    for account in list_accounts({}):
        yield account.name
