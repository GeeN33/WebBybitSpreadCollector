from django.core.management.base import BaseCommand, CommandError

from collector.services import upDataFundingStart

class Command(BaseCommand):
    help = 'updatafunding'

    def handle(self, *args, **options):
        upDataFundingStart()