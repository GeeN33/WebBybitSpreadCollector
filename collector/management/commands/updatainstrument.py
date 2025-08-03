from django.core.management.base import BaseCommand, CommandError

from collector.services import upDataInstrument

class Command(BaseCommand):
    help = 'updatainstrument'

    def handle(self, *args, **options):
        upDataInstrument()
