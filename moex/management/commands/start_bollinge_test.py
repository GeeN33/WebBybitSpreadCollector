from django.core.management.base import BaseCommand, CommandError

from moex.services import startBollinger


class Command(BaseCommand):
    help = 'start_bollinge_test'

    def handle(self, *args, **options):
        startBollinger("CNY")