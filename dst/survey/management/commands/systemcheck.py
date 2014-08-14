from django.core.management.base import BaseCommand, CommandError
from survey.validate import systemcheck, SystemCheckError


class Command(BaseCommand):
    help = 'Checks the current system for data integrity'

    def handle(self, *args, **options):
        try:
            systemcheck()
        except SystemCheckError as error:
            raise CommandError(error)

        self.stdout.write('Successfully checked system!')
