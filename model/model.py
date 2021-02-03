from typing import List, Optional
from datetime import date, datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int


class Batch:

    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference: str = ref
        self.sku: str = sku
        self.available_quantity: int = qty
        self.eta: Optional[date] = eta

    def allocate(self, line: OrderLine) -> bool:
        if line.qty > self.available_quantity:
            raise Exception("Cannot order my items than in stock")
        else:
            self.available_quantity -= line.qty





