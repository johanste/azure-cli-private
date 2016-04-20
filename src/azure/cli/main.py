﻿import os
import sys

from .application import Application, Configuration

from ._logging import configure_logging, logger
from ._session import Session
from ._output import OutputProducer

#ACCOUNT contains subscriptions information
# this file will be shared with azure-xplat-cli, which assumes ascii
ACCOUNT = Session('ascii')

# CONFIG provides external configuration options
CONFIG = Session()

# SESSION provides read-write session variables
SESSION = Session()

def main(args, file=sys.stdout): #pylint: disable=redefined-builtin
    azure_folder = os.path.expanduser('~/.azure')
    if not os.path.exists(azure_folder):
        os.makedirs(azure_folder)
    ACCOUNT.load(os.path.join(azure_folder, 'azureProfile.json'))
    CONFIG.load(os.path.join(azure_folder, 'az.json'))
    SESSION.load(os.path.join(azure_folder, 'az.sess'), max_age=3600)

    configure_logging(args, CONFIG)

    from ._locale import install as locale_install
    locale_install(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'locale',
                                CONFIG.get('locale', 'en-US')))

    try:
        config = Configuration(args)
        app = Application(config)
        cmd_result = app.execute(args)
        # Commands can return a dictionary/list of results
        # If they do, we print the results.
        if cmd_result:
            formatter = OutputProducer.get_formatter(app.configuration.output_format)
            OutputProducer(formatter=formatter, file=file).out(cmd_result)
    except KeyboardInterrupt:
        return 130 # 128 + SIGINT
    except RuntimeError as ex:
        logger.error(ex.args[0])
        return ex.args[1] if len(ex.args) >= 2 else -1
    except Exception as ex:
        logger.error(ex)
        return 1 # General error
