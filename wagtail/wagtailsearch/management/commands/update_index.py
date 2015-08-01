from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from wagtail.wagtailsearch.index import get_indexed_models
from wagtail.wagtailsearch.backends import get_search_backend


class Command(BaseCommand):
    def get_object_list(self):
        # Return list of (model_name, queryset) tuples
        return [
            (model, model.get_indexed_objects())
            for model in get_indexed_models()
        ]

    def update_backend(self, backend_name, object_list):
        # Print info
        self.stdout.write("Updating backend: " + backend_name)

        # Get backend
        backend = get_search_backend(backend_name)

        # Get rebuilder
        rebuilder = backend.get_rebuilder()

        if not rebuilder:
            self.stdout.write(backend_name + ": Backend doesn't support rebuild. Skipping")
            return

        # Start rebuild
        self.stdout.write(backend_name + ": Starting rebuild")
        rebuilder.start()

        for model, queryset in object_list:
            self.stdout.write(backend_name + ": Indexing model '%s.%s'" % (
                model._meta.app_label,
                model.__name__,
            ))

            # Add model
            rebuilder.add_model(model)

            # Add items
            rebuilder.add_items(model, queryset)

        # Finish rebuild
        self.stdout.write(backend_name + ": Finishing rebuild")
        rebuilder.finish()

    option_list = BaseCommand.option_list + (
        make_option('--backend',
            action='store',
            dest='backend_name',
            default=None,
            help="Specify a backend to update",
        ),
    )

    def handle(self, **options):
        # Get object list
        object_list = self.get_object_list()

        # Get list of backends to index
        if options['backend_name']:
            # index only the passed backend
            backend_names = [options['backend_name']]
        elif hasattr(settings, 'WAGTAILSEARCH_BACKENDS'):
            # index all backends listed in settings
            backend_names = settings.WAGTAILSEARCH_BACKENDS.keys()
        else:
            # index the 'default' backend only
            backend_names = ['default']

        # Update backends
        for backend_name in backend_names:
            self.update_backend(backend_name, object_list)
