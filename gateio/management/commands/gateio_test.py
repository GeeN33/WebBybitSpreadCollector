from django.core.management.base import BaseCommand, CommandError

from gateio.services import upDataInstrumentGateio, upDataBarSpreadGateioStart


class Command(BaseCommand):
    help = 'gateio_test'

    def handle(self, *args, **options):
        # upDataInstrumentGateio()
        upDataBarSpreadGateioStart()