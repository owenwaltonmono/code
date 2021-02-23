from unittest import TestCase
from datetime import date, timedelta
import pytest

import attr

from model.model import Batch, OrderLine, allocate, OutOfStock

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
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest_batch = Batch("speedy-batch", "MINIMALIST_SPOON", 100, eta=today)
    medium_batch = Batch("normal-batch", "MINIMALIST_SPOON", 100, eta=tomorrow)
    latest_batch = Batch("slow-batch", "MINIMALIST_SPOON", 100, eta=later)
    line = OrderLine("order1", "MINIMALIST_SPOON", 10)

    allocate(line, [earliest_batch, medium_batch, latest_batch])

    assert earliest_batch.available_quantity == 90
    assert medium_batch.available_quantity == 100
    assert latest_batch.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=today)
    shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=tomorrow)
    line = OrderLine("oref", "HIGHBROW_POSTER", 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception():
    batch = Batch("batch1", "SMALL_FORK", 10, eta=today)
    allocate(OrderLine("order1", "SMALL_FORK", 10), [batch])

    with pytest.raises(OutOfStock, match="SMALL_FORK"):
        allocate(OrderLine("order2", "SMALL_FORK", 1), [batch])
