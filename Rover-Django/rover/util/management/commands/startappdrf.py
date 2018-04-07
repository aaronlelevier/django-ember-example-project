import os
from os import path

from django.core.management.commands.startapp import Command as StartAppCommand


class Command(StartAppCommand):
    help = (
        "Creates a Django app with a dir and file structure more "
        "suitable for djang-rest-framework"
    )
    missing_args_message = "app name required"

    def handle(self, **options):
        super(Command, self).handle(**options)

        app_name = options.get('name')
        app_dir = path.join(os.getcwd(), app_name)

        # remove files
        os.remove(path.join(app_dir, 'tests.py'))

        # add files
        with open(path.join(app_dir, 'serializers.py'), 'w') as f: pass

        test_dir = path.join(app_dir, 'tests')
        os.mkdir(test_dir)

        for file in ['__init__.py', 'test_models.py', 'test_views.py']:
            with open(path.join(test_dir, file), 'w') as f: pass
