from celery import shared_task

from moex_smart_order.services import startSmartBot


@shared_task
def StartSmartBot_Task(name):
    startSmartBot(name)