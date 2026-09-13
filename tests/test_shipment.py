from unittest import result
from src.tool.shipment_analysis import (
    shipment_summary,
    delivery_performance,
    carrier_performance,
    shipment_status_analysis,
)

from src import ShipmentController

def test_shipment_summary():
    result = shipment_summary()

    assert result["total_shipments"] == 154
    assert result["evaluable_shipments"] == 108
    assert result["delayed_shipments"] == 0
    assert result["on_time_shipments"] == 106
    assert result["early_shipments"] == 2
    assert result["delay_rate"] == 0.0
    assert result["unique_carriers"] == 16

def test_delivery_performance():
    result = delivery_performance()

    assert isinstance(result, list)
    assert len(result) == 108

    statuses = {
        item["delivery_status"]
        for item in result
    }

    assert statuses.issubset({"delayed", "on_time", "early"})

    early_shipments = [
        item
        for item in result
        if item["delivery_status"] == "early"
    ]

    assert len(early_shipments) == 2


def test_carrier_performance():
    result = carrier_performance()

    assert isinstance(result, list)
    assert len(result) ==15

    total_evaluated = sum(item["total_shipments"] for item in result)

    assert total_evaluated == 108

    first_item = result[0]

    assert "carrier_name" in first_item
    assert "delay_rate" in first_item
    assert "on_time_rate" in first_item

def test_shipment_status_analysis():
    result = shipment_status_analysis()

    status_counts = {
        item["status"]: item["shipment_count"]
        for item in result
    }

    assert status_counts["completed"] == 108
    assert status_counts["incomplete"] == 46

def test_shipment_controller_summary():
    controller = ShipmentController()


    result = controller.execute(
        {
            "analysis_type": "summary"
        }
    )

    assert result["total_shipments"] == 154
    assert result["evaluable_shipments"] == 108
    assert result["delayed_shipments"] == 0