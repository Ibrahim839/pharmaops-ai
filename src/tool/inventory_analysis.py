import pandas as pd
from pathlib import Path


DATA_PATH = (
    Path(__file__).resolve().parent.parent
    /"assets"
    / "data"
    / "pharmaceutical-inventory-supply-chains.csv"
)


def load_data():
    """Load the pharmaceutical supply-chain dataset."""
    df = pd.read_csv(DATA_PATH)

    # Convert date columns
    date_columns = [
        "order_date",
        "expiration_date",
        "shipment_date",
        "expected_delivery_date",
        "actual_delivery_date",
        "storage_entry_date",
        "storage_exit_date",
        "last_updated",
    ]

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce", utc=True)

    return df


def inventory_summary():
    """Return an overall inventory summary."""
    df = load_data()

    return {
        "total_records": int(len(df)),
        "total_inventory": float(df["current_inventory_level"].sum()),
        "average_inventory": float(df["current_inventory_level"].mean()),
        "stockout_events": int(df["stockout_flag"].sum()),
        "stockout_rate": float(df["stockout_flag"].mean()),
        "unique_products": int(df["product_id"].nunique()),
        "unique_facilities": int(df["destination_facility_id"].nunique()),
    }


def stockout_analysis():
    """Analyze stockouts by product."""
    df = load_data()

    result = (
        df.groupby(["product_id", "product_name"],dropna=False)
        .agg(
            records=("order_id", "count"),
            stockouts=("stockout_flag", "sum"),
            average_inventory=("current_inventory_level", "mean"),
            total_quantity_ordered=("quantity_ordered", "sum"),
        )
        .reset_index()
    )

    result["stockout_rate"] = result["stockouts"] / result["records"]

    result = result.sort_values(["stockouts", "stockout_rate"], ascending=[False,False])

    return result.to_dict(orient="records")


def low_inventory_products(threshold=20):
    """Find products whose current inventory is below a threshold."""
    df = load_data()

    result = df[df["current_inventory_level"] < threshold][
        [
            "product_id",
            "product_name",
            "current_inventory_level",
            "stockout_flag",
            "destination_facility_name",
        ]
    ].copy()

    result = result.sort_values("current_inventory_level")

    return result.to_dict(orient="records")


def expiration_risk(days=90):
    """Find batches approaching expiration."""
    df = load_data()

    today = pd.Timestamp.now(tz="UTC")
    cutoff = today + pd.Timedelta(days=days)

    result = df[
        (df["expiration_date"].notna())
        & (df["expiration_date"] >= today)
        & (df["expiration_date"] <= cutoff)
    ][
        [
            "product_id",
            "product_name",
            "batch_number",
            "expiration_date",
            "current_inventory_level",
            "destination_facility_name",
        ]
    ].copy()

    result = result.sort_values("expiration_date")

    result["expiration_date"] = result["expiration_date"].dt.strftime(
        "%Y-%m-%d"
    )


    return result.to_dict(orient="records")


 
if __name__ == "__main__":
    print("=== Inventory Summary ===")
    print(inventory_summary())

    print("\n=== Stockout Analysis ===")
    for item in stockout_analysis():
        print(item)

    print("\n=== Low Inventory Products ===")
    for item in low_inventory_products():
        print(item)

    print("\n=== Expiration Risk ===")
    for item in expiration_risk():
        print(item)
