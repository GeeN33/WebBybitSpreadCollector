from celery import shared_task

from collector.services import upDataInstrument, upDataBarSpreadStart, upDataFundingStart


@shared_task
def up_Data_Instrument():
    upDataInstrument()


@shared_task
def up_Data_Bar_Spread_Start():
    res = upDataBarSpreadStart()
    return res



@shared_task
def up_Data_Funding_Start():
    res = upDataFundingStart()
    return res