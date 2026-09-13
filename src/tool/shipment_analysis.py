import pandas as pd 
from pathlib import Path


DATA_PATH = (Path(__file__).resolve().parent.parent / "assets"/ "data"/ "pharmaceutical-inventory-supply-chains.csv" )


def load_data():
    """
    load the pharmaceutical supply chain datasets
    and prepare shipment related date  columns
    """

    df = pd.read_csv(DATA_PATH)


    data_columns = [
        "shipment_date",
        "expected_delivery_date",
        "actual_delivery_date",
    ]

    for column in data_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column],errors="coerce", utc=True)

    return df

def shipment_summary():
    """
    return a high level summary of shipment activity
    """

    df = load_data()

    shipments = df[df["shipment_id"].notna()].copy()

    evaluable_shipments = shipments[
        shipments["expected_delivery_date"].notna()
        & shipments["actual_delivery_date"].notna()
    ].copy()

    evaluable_shipments["delay_days"] = (evaluable_shipments["actual_delivery_date"]- evaluable_shipments["expected_delivery_date"]).dt.days

    delayed_shipments = (evaluable_shipments["delay_days"] > 0).sum()

    on_time_shipments = (evaluable_shipments["delay_days"] == 0).sum()

    early_shipments = (evaluable_shipments["delay_days"] < 0).sum()

    

    return {
        "total_shipments": int(len(shipments)),
        "evaluable_shipments": int(len(evaluable_shipments)),
        "delayed_shipments": int(delayed_shipments),
        "on_time_shipments": int(on_time_shipments),
        "early_shipments": int(early_shipments),
        "delay_rate": float(delayed_shipments / len(evaluable_shipments)) if len(evaluable_shipments) > 0 else None,"unique_carriers": int(shipments["carrier_name"].nunique()),
        "unique_carriers": int(
            shipments["carrier_name"].nunique()
        ),
    }


def delivery_performance():
    """
    Analyxe delivery performance for shipments
    that have both expected and actual delivery dates.
    """

    df = load_data()

    shipments = df[df["shipment_id"].notna() & df["expected_delivery_date"].notna() & df["actual_delivery_date"].notna()].copy()


    shipments["delay_days"] = (shipments["actual_delivery_date"] - shipments["expected_delivery_date"]).dt.days

    shipments["delivery_status"] = shipments["delay_days"].apply(
        lambda days: (
            "delayed"
            if days > 0
            else "early"
            if days < 0
            else "on_time"
            )
        )

    result = shipments[
        [
            "shipment_id",
            "carrier_name",
            "expected_delivery_date",
            "actual_delivery_date",
            "delay_days",
            "delivery_status",
            "destination_facility_name",
        ]

    ].copy()

    result["expected_delivery_date"] = (result["expected_delivery_date"].dt.strftime("%Y-%m-%d"))
    result["actual_delivery_date"] = (result["actual_delivery_date"].dt.strftime("%Y-%m-%d"))

    return result.to_dict(orient="records")    


def carrier_performance():
    """
    Analyze delivery performance for each carrier
    """
    df = load_data()
    
    shipments = df[
        df["shipment_id"].notna()
        & df["carrier_name"].notna()
        & df["expected_delivery_date"].notna()
        & df["actual_delivery_date"].notna()].copy()

    shipments["delay_days"] = (
        shipments["actual_delivery_date"]
        - shipments["expected_delivery_date"]
    ).dt.days

    shipments["is_delayed"] = shipments["delay_days"] > 0
    shipments["is_on_time"] = shipments["delay_days"] == 0
    shipments["is_early"] = shipments["delay_days"] < 0

    result = (shipments.groupby("carrier_name").agg(
        total_shipments=("shipment_id", "count"),
        delayed_shipments=("is_delayed", "sum"),
        on_time_shipments=("is_on_time", "sum"),
        early_shipments=("is_early", "sum"),
        average_delay_days=("delay_days", "mean")
        ).reset_index()

    )

    result["delay_rate"] = (result["delayed_shipments"] / result["total_shipments"])

    result["on_time_rate"] = (result["on_time_shipments"] / result["total_shipments"])
    
    result = result.sort_values(["delay_rate", "on_time_rate"], ascending=[True,False])

    return result.to_dict(orient="records")



def shipment_status_analysis():
    """
    Analyze shipment data completeness based on
    available expected and actual delivery dates.    
    """

    df = load_data()

    shipments = df[df["shipment_id"].notna()].copy()

    shipments["has_expected_date"] = (shipments["expected_delivery_date"].notna())

    shipments["has_actual_date"] = (shipments["actual_delivery_date"].notna())

    shipments["status"] = "incomplete"

    shipments.loc[shipments["has_expected_date"]& shipments["has_actual_date"],"status"] = "completed"

    result = (shipments.groupby("status").agg(shipment_count=("shipment_id", "count")).reset_index())


    return result.to_dict(orient="records")