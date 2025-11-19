from django.core.management.base import BaseCommand, CommandError

from moex_smart_order.services import startSmartBot


class Command(BaseCommand):
    help = 'start_bot_smart_test'

    def handle(self, *args, **options):
        startSmartBot('CNY-spread')