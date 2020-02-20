import staticconf
from django.core.management.base import BaseCommand, CommandError
from ussdframework.core import UssdView, load_yaml
import os
import json


class Command(BaseCommand):
    help = 'Validate ussdframework customer journey'

    def add_arguments(self, parser):
        parser.add_argument('ussd_configs', nargs='+', type=str)

    def handle(self, *args, **options):
        error_message = {}
        for ussd_config in options["ussd_configs"]:
            if not os.path.isfile(ussd_config):
                raise CommandError("This file path {} does not exist".format(ussd_config))
            namespace = 'validation'
            load_yaml(ussd_config, namespace)


            ussd_screens = staticconf.config. \
                get_namespace(namespace). \
                get_config_values()

            is_valid, error_ussd_config_message = UssdView.validate_ussd_journey(
                ussd_screens)
            error_message[ussd_config] = dict(
                valid=is_valid,
                error_message=error_ussd_config_message
            )
            if not is_valid:
                raise CommandError(json.dumps(error_message))

        self.stdout.write(json.dumps(error_message))
