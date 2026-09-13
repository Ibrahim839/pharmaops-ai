from src.tool.inventory_analysis import (
    inventory_summary,
    stockout_analysis,
    low_inventory_products,
    expiration_risk,
)

from src.controllers.inventorycontroller import InventoryController


def test_inventory_summary():
    result = inventory_summary()

    assert result["total_records"] == 200
    assert result["total_inventory"] == 399197.0
    assert result["stockout_events"] == 26
    assert result["stockout_rate"] == 0.13
    assert result["unique_products"] == 132
    assert result["unique_facilities"] == 178


def test_stockout_analysis():
    result = stockout_analysis()

    assert isinstance(result, list)
    assert len(result) > 0

    first_item = result[0]

    assert "product_id" in first_item
    assert "stockouts" in first_item
    assert "stockout_rate" in first_item


def test_low_inventory_products():
    result = low_inventory_products(threshold=20)

    assert isinstance(result, list)

    for item in result:
        assert item["current_inventory_level"] < 20


def test_expiration_risk():
    result = expiration_risk(days=90)

    assert isinstance(result, list)

    for item in result:
        assert "expiration_date" in item


def test_inventory_controller_summary():
    controller = InventoryController()

    result = controller.execute(
        {
            "analysis_type": "summary"
        }
    )

    assert result["total_records"] == 200
    assert result["stockout_events"] == 26