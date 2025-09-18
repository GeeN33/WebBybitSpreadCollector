from django.core.management.base import BaseCommand, CommandError

from moex.services import startBot


class Command(BaseCommand):
    help = 'start_bot_test'

    def handle(self, *args, **options):
        startBot("CNY")