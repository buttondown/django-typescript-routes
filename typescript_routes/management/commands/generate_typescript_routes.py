from typescript_routes.lib.logic import generate_routes
from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser


class Command(BaseCommand):
    help = 'Prints a static TypeScript file that can be used to reverse Django URLs.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-u", "--urlconf", type=str)
        parser.add_argument("-i", "--ignore", nargs="*", type=str)

    def handle(self, *args, **options):
        urlconf = options["urlconf"]
        ignore = options["ignore"] or []
        self.stdout.write(generate_routes(urlconf, ignore))
