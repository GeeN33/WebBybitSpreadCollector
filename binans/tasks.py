from celery import shared_task

from binans.services import upDataBarSpreadBinansStart

@shared_task
def up_Binansa_Bar_Spread_Start():
    res = upDataBarSpreadBinansStart()
    return res