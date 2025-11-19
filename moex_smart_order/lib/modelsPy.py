from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class Order(BaseModel):
    order_id: str
    account_id: str
    symbol: str
    side: str
    status: str
    order_type: str
    limit_price: float
    quantity: float