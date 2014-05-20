from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from hlidskjalf.evals.movies import MoviesEval


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-u', '--url', action='store', dest='url', help='Entry point'),
        make_option('-n', '--name', action='store', dest='name', help='Set name'),
        make_option('-m', '--more', action='store_true', dest='verbose', default=False, help='Verbose output'),
        make_option('-t', '--threads', action='store', type=int, dest='threads', default=5, help='Threads number'),
    )

    def handle(self, *args, **options):
        if not options['url'] or not options['name']:
            raise CommandError('Entry point and set name are necessary')

        tool = MoviesEval()
        tool.set_entry_point(options['url'])
        result = tool.run(options['name'], options['threads'])
        if options['verbose']:
            self.stdout.write("Result: %s" % result)