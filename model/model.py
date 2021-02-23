from typing import List, Optional
from datetime import date, datetime
from dataclasses import dataclass

"""Exceptions"""


class OutOfStock(Exception):
    pass


""" Value objects vs Entities"""

# Value object
# business concept with data but no identity often choose to represent using Value Object pattern
# immutable and uniquely identified by data it holds
@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int


# Entity
# Domain object with a long-lived identity

class Batch:

    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference: str = ref
        self.sku: str = sku
        self._purchased_quantity: int = qty
        self._allocations: set = set()
        self.eta: Optional[date] = eta

    def __eq__(self, other):
        """
        Defines the behaviour for the == operator
        :param other:
        :return:
        """
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        """
        Implementation of the > operator, greater than = gt
        :param other:
        :return:
        """
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

    @property
    def allocated_quantity(self):
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self):
        return self._purchased_quantity - self.allocated_quantity


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku: {line.sku}")
