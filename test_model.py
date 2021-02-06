from unittest import TestCase
from datetime import date, timedelta
import pytest

import attr

from model.model import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


# setup functions
def make_batch_and_line(sku: str, batch_qty: int, line_qty: int):
    return (
        Batch("batch-001", sku, qty=batch_qty, eta=date.today()),
        OrderLine('order-ref', sku, line_qty)
    )


""" Test Batch Object """


def test_allocating_to_a_batch_reduces_the_available_quantity():
    large_batch, small_line = make_batch_and_line("SMALL-TABLE", 20, 2)
    large_batch.can_allocate(small_line)
    large_batch.allocate(small_line)
    assert 18 == large_batch.available_quantity


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("SMALL-TABLE", 20, 2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("SMALL-TABLE", 20, 22)
    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("SMALL-TABLE", 20, 20)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "LARGE_CHAIR", qty=20, eta=date.today())
    line = OrderLine('order-ref', "SMALL_TABLE", 2)
    assert batch.can_allocate(line) is False


def test_can_only_deallocate_allocated_lines():
    large_batch, small_line = make_batch_and_line("SMALL-TABLE", 20, 2)
    large_batch.deallocate(small_line)
    assert large_batch.available_quantity == 20


def test_allocation_is_idempotent():
    large_batch, small_line = make_batch_and_line("SMALL-TABLE", 20, 2)
    large_batch.allocate(small_line)
    large_batch.allocate(small_line)
    assert large_batch.available_quantity == 18


""" Test Allocator Function """


def test_prefers_warehouse_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment_batch", "RETRO-CLOCK", 100, eta=tomorrow)


def test_prefers_earlier_batches():
    pytest.fail('todo')

