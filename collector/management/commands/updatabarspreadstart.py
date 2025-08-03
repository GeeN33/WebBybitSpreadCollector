from django.core.management.base import BaseCommand, CommandError

from collector.services import upDataBarSpreadStart

class Command(BaseCommand):
    help = 'updatabarspreadstart'

    def handle(self, *args, **options):
        upDataBarSpreadStart()