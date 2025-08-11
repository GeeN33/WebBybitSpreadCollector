from celery import shared_task

from gateio.services import upDataInstrumentGateio, upDataBarSpreadGateioStart


@shared_task
def up_Data_Instrument_Gateio():
    res = upDataInstrumentGateio()
    return res

@shared_task
def up_Data_BarSpread_Gateio_Start():
    res = upDataBarSpreadGateioStart()
    return res