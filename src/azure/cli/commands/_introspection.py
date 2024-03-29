import inspect
import re

def _option_descriptions(operation):
    """Pull out parameter help from doccomments of the command
    """
    option_descs = {}
    lines = inspect.getdoc(operation)
    if lines:
        lines = lines.splitlines()
        index = 0
        while index < len(lines):
            l = lines[index]
            regex = r'\s*(:param)\s+(.+)\s*:(.*)'
            match = re.search(regex, l)
            if match:
                # 'arg name' portion might have type info, we don't need it
                arg_name = str.split(match.group(2))[-1]
                arg_desc = match.group(3).strip()
                #look for more descriptions on subsequent lines
                index += 1
                while index < len(lines):
                    temp = lines[index].strip()
                    if temp.startswith(':'):
                        break
                    else:
                        if temp:
                            arg_desc += (' ' + temp)
                        index += 1

                option_descs[arg_name] = arg_desc
            else:
                index += 1
    return option_descs

EXCLUDED_PARAMS = frozenset(['self', 'raw', 'custom_headers', 'operation_config',
                             'content_version', 'kwargs', 'client'])

def extract_args_from_signature(command, operation):
    """ Extracts basic argument data from an operation's signature and docstring """
    args = []
    try:
        # only supported in python3 - falling back to argspec if not available
        sig = inspect.signature(operation)
        args = sig.parameters
    except AttributeError:
        sig = inspect.getargspec(operation) #pylint: disable=deprecated-method
        args = sig.args

    arg_docstring_help = _option_descriptions(operation)
    for arg_name in [a for a in args if not a in EXCLUDED_PARAMS]:
        try:
            # this works in python3
            default = args[arg_name].default
            required = default == inspect.Parameter.empty #pylint: disable=no-member
        except TypeError:
            arg_defaults = (dict(zip(sig.args[-len(sig.defaults):], sig.defaults))
                            if sig.defaults
                            else {})
            default = arg_defaults.get(arg_name)
            required = arg_name not in arg_defaults

        action = 'store_' + str(not default).lower() if isinstance(default, bool) else None

        try:
            default = (default
                       if default != inspect._empty #pylint: disable=protected-access, no-member
                       else None)
        except AttributeError:
            pass

        command.add_argument(arg_name,
                             *['--' + arg_name.replace('_', '-')],
                             required=required,
                             default=default,
                             help=arg_docstring_help.get(arg_name),
                             action=action)

