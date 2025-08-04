from django.core.management.base import BaseCommand, CommandError

from binans.services import upDataBarSpreadBinansStart


class Command(BaseCommand):
    help = 'upDataBarspreadBinansstart'

    def handle(self, *args, **options):
        upDataBarSpreadBinansStart()