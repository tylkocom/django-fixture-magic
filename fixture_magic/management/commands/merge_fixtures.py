from __future__ import print_function

import json

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Merge a series of fixtures and remove duplicates.'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='files', nargs='+', help='One or more fixture.')

    def handle(self, *files, **options):
        """
        Load a bunch of json files.  Store the pk/model in a seen dictionary.
        Add all the unseen objects into output.
        """
        output = []
        seen = set()

        for file_ in files:
            with open(file_, 'w') as fp:
                data = json.load(fp)
            for obj in data:
                key = '{}|{}'.format(
                    obj.get('model'),
                    obj.get('pk')
                )
                if key not in seen:
                    seen.add(key)
                    output.append(obj)

        print(json.dumps(output, sort_keys=True, indent=4))
