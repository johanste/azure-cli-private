from __future__ import print_function
import sys
from six.moves import input #pylint: disable=redefined-builtin
import azure.cli as cli
from azure.cli.commands import cli_command
import azure.cli._logging as _logging

logger = _logging.get_az_logger(__name__)

MESSAGES = {
    'intro': 'We appreciate your feedback! This survey is only two questions and should take less '\
             'than a minute.',
    'prompt_how_likely': '\nHow likely is it you would recommend our Azure CLI to a friend or '\
                         'colleague? [0 to 10]: ',
    'prompt_what_changes': '\nWhat changes would we have to make for you to give us a higher '\
                           'rating? ',
    'prompt_do_well': '\nWhat do we do really well? ',
    'prompt_email_addr': '\nIf you would like to join our insiders program and receive tips, '\
                         'tricks, and early access to new features, let us know by leaving your '\
                         'email address (leave blank to skip): ',
    'thanks': '\nThanks for your feedback!'
}

INSTRUMENTATION_KEY = '02b91c82-6729-4241-befc-e6d02ca4fbba'
EVENT_NAME = 'FeedbackEvent'

COMPONENT_PREFIX = 'azure-cli-'

def _prompt_net_promoter_score():
    while True:
        try:
            score = int(input(MESSAGES['prompt_how_likely']))
            if 0 <= score <= 10:
                return score
            raise ValueError
        except ValueError:
            logger.warning('Valid values are %s', list(range(11)))

def _get_version_info():
    from pip import get_installed_distributions
    installed_dists = get_installed_distributions(local_only=True)

    component_version_info = sorted([{'name': dist.key.replace(COMPONENT_PREFIX, ''),
                                      'version': dist.version}
                                     for dist in installed_dists
                                     if dist.key.startswith(COMPONENT_PREFIX)],
                                    key=lambda x: x['name'])
    return str(component_version_info), sys.version

def _send_feedback(score, response_what_changes, response_do_well, email_address):
    from applicationinsights import TelemetryClient
    tc = TelemetryClient(INSTRUMENTATION_KEY)
    tc.context.application.ver = cli.__version__ #pylint: disable=no-member
    version_components, version_python = _get_version_info()
    tc.track_event(
        EVENT_NAME,
        {'response_what_changes': response_what_changes,
         'response_do_well': response_do_well,
         'response_email_address': email_address,
         'version_components': version_components,
         'version_python': version_python},
        {'response_net_promoter_score':score})
    tc.flush()

def handle_feedback():
    try:
        print(MESSAGES['intro'])
        score = _prompt_net_promoter_score()
        response_do_well = None
        response_what_changes = None
        if score == 10:
            response_do_well = input(MESSAGES['prompt_do_well'])
        else:
            response_what_changes = input(MESSAGES['prompt_what_changes'])
        email_address = input(MESSAGES['prompt_email_addr'])
        _send_feedback(score, response_what_changes, response_do_well, email_address)
        print(MESSAGES['thanks'])
    except KeyboardInterrupt:
        # Catch to prevent stacktrace and print newline
        print()

cli_command('feedback', handle_feedback)
