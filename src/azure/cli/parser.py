import argparse

class IncorrectUsageError(Exception):
    '''Raised when a command is incorrectly used and the usage should be
    displayed to the user.
    '''
    pass

class AzCliCommandParser(argparse.ArgumentParser):
    """ArgumentParser implementation specialized for the
    Azure CLI utility.
    """
    def __init__(self, **kwargs):
        super(AzCliCommandParser, self).__init__(**kwargs)
        self.subparsers = {}
        self.parents = kwargs.get('parents', None)

    def load_command_table(self, session, command_table):
        """Load a command table into our parser.
        """
        # If we haven't already added a subparser, we
        # better do it.
        if not self.subparsers:
            sp = self.add_subparsers(dest='_command_package')
            sp.required = True
            self.subparsers = {(): sp}

        for handler, metadata in command_table.items():
            subparser = self._get_subparser(metadata['name'].split())
            command_name = metadata['name'].split()[-1]
            # To work around http://bugs.python.org/issue9253, we artificially add any new
            # parsers we add to the "choices" section of the subparser.
            subparser.choices[command_name] = command_name
            command_parser = subparser.add_parser(command_name, description=metadata.get('description'), parents=self.parents)
            session.raise_event('AzCliCommandParser.SubparserCreated',
                                {'parser': command_parser, 'metadata': metadata})
            for arg in metadata['options']:
                command_parser.add_argument(*arg.pop('name'),
                                            **arg)
            command_parser.set_defaults(func=handler)

    def _get_subparser(self, path):
        """For each part of the path, walk down the tree of
        subparsers, creating new ones if one doesn't already exist.
        """
        for length in range(0, len(path)):
            parent_subparser = self.subparsers.get(tuple(path[0:length]), None)
            if not parent_subparser:
                # No subparser exists for the given subpath - create and register
                # a new subparser.
                # Since we know that we always have a root subparser (we created)
                # one when we started loading the command table, and we walk the
                # path from left to right (i.e. for "cmd subcmd1 subcmd2", we start
                # with ensuring that a subparser for cmd exists, then for subcmd1,
                # subcmd2 and so on), we know we can always back up one step and
                # add a subparser if one doesn't exist
                grandparent_subparser = self.subparsers[tuple(path[0:length - 1])]
                new_parser = grandparent_subparser.add_parser(path[length - 1])

                # Due to http://bugs.python.org/issue9253, we have to give the subparser
                # a destination and set it to requried in order to get a meaningful error
                parent_subparser = new_parser.add_subparsers(dest='subcommand')
                parent_subparser.required = True
                self.subparsers[tuple(path[0:length])] = parent_subparser
        return parent_subparser