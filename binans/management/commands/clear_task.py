from django.core.management.base import BaseCommand, CommandError
from django_celery_results.models import TaskResult



class Command(BaseCommand):
    help = 'clear_task'

    def handle(self, *args, **options):
        TaskResult.objects.all().delete()