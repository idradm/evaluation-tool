from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from hlidskjalf.importer import Importer


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-i', '--input', action='store', dest='file', default=False, help='Input file'),
        make_option('-n', '--name', action='store', dest='name', default=False, help='Set name'),
        make_option('-m', '--more', action='store_true', dest='verbose', default=False, help='Verbose output'),
    )

    def handle(self, *args, **options):
        if not options['file'] or not options['name']:
            raise CommandError('File and set name are necessary')

        result = Importer(options['name'], options['file']).run()
        if options['verbose']:
            self.stdout.write("Added: %s" % result)